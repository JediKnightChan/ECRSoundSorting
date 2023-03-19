<template>
  <CCard v-for="post in original_api_data" :key="post.id">
    <CCardHeader><span class="m-2">Федор Иванов</span></CCardHeader>
    <CCardBody class="mx-2 my-4">
      <CCardTitle>{{ post.title }}</CCardTitle>
      <CCardText>{{ post.text }}</CCardText>
    </CCardBody>
  </CCard>
</template>

<script>
import APIMixin from '@/common/mixins/APIListMixin.vue'
import { GENERAL_NEWS_API_HOOK } from '@/common/api_endpoints'

export default {
  name: 'Blog',
  mixins: [APIMixin],
  data() {
    return {
      loading_mode: 'pagination',
      api_first_page_link: GENERAL_NEWS_API_HOOK,
    }
  },
}
</script>

<style scoped></style>
