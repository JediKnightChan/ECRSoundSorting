<script>
import { format_url_with_get_params } from '@/common/utils'
import { fetch_api_json } from '@/common/api_endpoints'

export default {
  name: 'APIListMixin',
  data() {
    return {
      loading_mode: 'on_mounted_all',
      original_api_data: null,
      api_first_page_link: null,
      api_next_page_link: null,
      params_getter: null,

      total_item_count: null,
      loading: false,
      loaded_all_data: false,

      api_call_in_progress: false,
    }
  },
  methods: {
    async fetchPageFromAPI(params_getter = null) {
      let link
      if (this.api_next_page_link) {
        link = this.api_next_page_link
      } else {
        let api_params = null
        if (params_getter) {
          api_params = await params_getter()
        }
        link = format_url_with_get_params(this.api_first_page_link, api_params)
      }
      this.loading = true
      const res = await fetch_api_json(link)
      const data = await res.json()
      this.total_item_count = data.count

      if (this.original_api_data) {
        this.original_api_data.push(...data.results)
      } else {
        this.original_api_data = data.results
      }
      this.api_next_page_link = data.next
      this.loading = false
    },
    async afterPageLoad() {},
    async afterLoadedAllData() {},
    async fetchAllData(params_getter = null) {
      this.original_api_data = null
      this.loaded_all_data = false
      do {
        await this.fetchPageFromAPI(params_getter)
      } while (this.api_next_page_link)
      this.loaded_all_data = true
      await this.afterLoadedAllData()
    },
    async fetchNextPageIfOnBottom(params_getter = null) {
      let bottomOfWindow =
        document.documentElement.scrollTop + window.innerHeight ===
        document.documentElement.offsetHeight
      let no_scroll_exists = document.documentElement.offsetHeight === 0
      if ((bottomOfWindow || no_scroll_exists) && !this.loading) {
        if (this.api_next_page_link) {
          await this.fetchPageFromAPI(params_getter)
          return true
        } else {
          await this.afterPageLoad()
          return false
        }
      }
      return false
    },
    async loadItemsUntilScroll(params_getter = null) {
      await this.fetchPageFromAPI(params_getter)
      let need_fetch = true
      do {
        need_fetch = await this.fetchNextPageIfOnBottom(params_getter)
      } while (need_fetch)
    },
    bindEndlessScroll() {
      window.onscroll = () => {
        this.fetchNextPageIfOnBottom()
      }
    },
    onObjectDeleted(data) {
      this.original_api_data = this.original_api_data.filter(
        (el) => el.id !== data.id,
      )
      this.total_item_count--
    },
    onObjectCreated(data) {
      if (this.original_api_data) {
        this.original_api_data.unshift(data)
      } else {
        this.original_api_data = [data]
      }
      this.total_item_count++
    },
    async make_api_call() {
      if (this.api_call_in_progress) {
        return
      }
      this.api_call_in_progress = true
      switch (this.loading_mode) {
        case 'on_mounted_all':
          await this.fetchAllData(this.params_getter)
          break
        case 'on_mounted_one':
          await this.fetchPageFromAPI(this.params_getter)
          break
        case 'pagination':
          await this.loadItemsUntilScroll(this.params_getter)
          this.bindEndlessScroll()
          break
        case 'custom':
          break
        default:
          break
      }
      this.api_call_in_progress = false
    },
  },
  computed: {
    loaded_item_count() {
      return this.original_api_data ? this.original_api_data.length : 0
    },
  },
  async mounted() {
    await this.make_api_call()
  },
}
</script>

<style scoped></style>
