<script>
import { format_url_with_get_params } from '@/common/utils'
import { fetch_api_json } from '@/common/api_endpoints'

export default {
  name: 'APIDetailMixin',
  data() {
    return {
      detail_api_data: null,
      detail_api_first_page_link: null,
      detail_params_getter: null,
    }
  },
  methods: {
    async fetchPageFromAPI(detail_params_getter = null) {
      let link
      let api_params = null
      if (detail_params_getter) {
        api_params = await detail_params_getter()
      }
      link = format_url_with_get_params(
        this.detail_api_first_page_link,
        api_params,
      )

      const res = await fetch_api_json(link)
      this.detail_api_data = await res.json()
    },
  },
  async mounted() {
    await this.fetchPageFromAPI(this.detail_params_getter)
  },
}
</script>

<style scoped></style>
