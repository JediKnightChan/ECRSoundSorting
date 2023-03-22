from rest_framework import serializers

from myauth.models import UserProfile
from .models import GameFolder, SoundItem, SoundCategory, SoundItemReview


class GameFolderSerializer(serializers.ModelSerializer):
    class Meta:
        model = GameFolder
        fields = ['id', 'name', 'type', 'parent_folder']


class SoundItemSerializer(serializers.ModelSerializer):
    sound_file = serializers.SerializerMethodField()
    gdrive_link = serializers.SerializerMethodField()

    class Meta:
        model = SoundItem
        fields = ['id', 'name', 'parent_folder', 'sound_file', 'gdrive_link', 'likes', 'dislikes']

    def get_sound_file(self, obj):
        if obj.gdrive_id:
            return f"https://drive.google.com/uc?id={obj.gdrive_id}&authuser=0&export=download"
        else:
            return ""

    def get_gdrive_link(self, obj):
        if obj.gdrive_id:
            return f"https://drive.google.com/uc?id={obj.gdrive_id}"
        else:
            return ""


class SoundCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = SoundCategory
        fields = ['id', 'name']


class SoundItemReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = SoundItemReview
        fields = ['id', 'sound', 'user_profile', 'is_useful', 'categories', 'text_review', 'created_ts', 'updated_ts']
        read_only_fields = ['created_ts', 'updated_ts', 'user_profile']

    def validate(self, attrs):
        request = self.context['request']

        profile = UserProfile.get_by_user(request.user)
        old_review = SoundItemReview.objects.filter(user_profile=profile, sound=attrs["sound"]).first()
        if old_review and request.method == 'POST':
            raise serializers.ValidationError("You already sent answer for this sound")

        sound = attrs['sound']
        if sound.parent_folder.type != GameFolder.GAME_TYPE:
            raise serializers.ValidationError("This sound cannot be reviewed")
        return attrs
