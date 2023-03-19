from rest_framework import viewsets, status

from rest_framework.fields import ListField
from rest_framework_mongoengine.fields import ReferenceField
from rest_framework.response import Response


class MongoModelFilterMixin(viewsets.ModelViewSet):
    fields_for_match_filter = []
    fields_for_contains_filter = []
    fields_for_in_range_filter = []

    @staticmethod
    def check_mongo_reference_field_is_valid(mongo_id, mongo_model_class):
        f = ReferenceField(model=mongo_model_class)
        return f.run_validation(data=mongo_id)

    def _check_filter_value_is_valid(self, filter_key, filter_value):
        m = self.serializer_class()
        validated_value = m.fields[filter_key].run_validation(filter_value)
        return validated_value

    def _field_is_list(self, filter_key):
        s = self.serializer_class()
        return isinstance(s.get_fields()[filter_key], ListField)

    def _filter_field_value_in_list(self, queryset, filter_key, filter_value_list):
        print(filter_key, filter_value_list)
        validated_values = [self._check_filter_value_is_valid(filter_key, filter_value)
                            for filter_value in filter_value_list]
        queryset = queryset.filter(
            **{filter_key + "__in": validated_values})
        return queryset

    def _filter_field_value(self, queryset, filter_key, filter_value, filter_suffix=""):
        if self._field_is_list(filter_key):
            filter_suffix = "__all"
        validated_value = self._check_filter_value_is_valid(filter_key, filter_value)
        queryset = queryset.filter(**{filter_key + filter_suffix: validated_value})
        return queryset

    def _get_single_value_or_list_from_query_params(self, filter_key):
        filter_value = self.request.query_params.getlist(filter_key)
        if len(filter_value) == 1:
            filter_value = filter_value[0]
        return filter_value

    def _filter_field_matches(self, queryset, filter_key):
        filter_value = self._get_single_value_or_list_from_query_params(filter_key)
        if filter_value:
            # We got list, but field isn't list, so this is a list 'should match at least 1 element'
            if isinstance(filter_value, list) and not self._field_is_list(filter_key):
                queryset = self._filter_field_value_in_list(queryset, filter_key, filter_value)
            else:
                queryset = self._filter_field_value(queryset, filter_key, filter_value)
        return queryset

    def _filter_field_contains(self, queryset, filter_key):
        filter_value = self.request.query_params.get(filter_key + "__contain")
        if filter_value is not None:
            queryset = self._filter_field_value(queryset, filter_key, filter_value, filter_suffix="__icontains")
        return queryset

    def _filter_field_in_range(self, queryset, filter_pair):
        first_key, last_key = filter_pair
        first_value, last_value = self.request.query_params.get(first_key + "__range"), \
                                  self.request.query_params.get(last_key + "__range")
        if last_value is not None:
            # start year (first_key) < provided end year (last_value)
            queryset = self._filter_field_value(queryset, first_key, last_value, filter_suffix="__lte")
        if first_value is not None:
            # end year (last_key) > provided first year (first_value)
            queryset = self._filter_field_value(queryset, last_key, first_value, filter_suffix="__gte")
        return queryset

    def filter_queryset_by_query_params(self, queryset):
        for key in self.fields_for_match_filter:
            queryset = self._filter_field_matches(queryset, key)
        for key in self.fields_for_contains_filter:
            queryset = self._filter_field_contains(queryset, key)
        for key in self.fields_for_in_range_filter:
            queryset = self._filter_field_in_range(queryset, key)
        return queryset


class MongoViewsetDeleteOnlyEmptyMixin(viewsets.ModelViewSet):
    children_model_class = None
    children_model_reference_name = None

    def destroy(self, request, *args, **kwargs):
        if not self.children_model_class:
            raise ValueError("Children model not specified")
        if not self.children_model_reference_name:
            raise ValueError("Reference name to this object in children not specified")

        instance = self.get_object()
        children_query = self.children_model_class.objects(**{self.children_model_reference_name: instance})
        if not children_query:
            # No children exist
            return super().destroy(request, *args, **kwargs)
        else:
            return Response({"error": "This model is referenced by its children"}, status=status.HTTP_409_CONFLICT)
