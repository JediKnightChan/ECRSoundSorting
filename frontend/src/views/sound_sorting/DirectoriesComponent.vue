<template>
  <DirectoryComponent
    v-if="parent_folder"
    :key="'dir_up'"
    :folder_id="parent_folder"
    :folder_name="'..'"
    :item_key="'dir_up'"
    @dir_clicked="on_dir_clicked"
  ></DirectoryComponent>
  <DirectoryComponent
    v-for="item in original_api_data"
    :key="item.id"
    :folder_id="item.id"
    :folder_name="item.name"
    :item_key="'dir' + item.id"
    @dir_clicked="on_dir_clicked"
  ></DirectoryComponent>
  <CenterSpinner v-if="loading"></CenterSpinner>
</template>

<script>
import DirectoryComponent from '@/views/sound_sorting/DirectoryComponent.vue'
import APIListMixin from '@/common/mixins/APIListMixin.vue'
import { GAME_FOLDERS_API_LINK } from '@/common/api_endpoints'
import { format_url_with_get_params } from '@/common/utils'
import CenterSpinner from '@/components/CenterSpinner.vue'

export default {
  name: 'DirectoriesComponent',
  props: {
    current_folder: {},
    parent_folder: {
      type: String,
    },
  },
  mixins: [APIListMixin],
  components: { CenterSpinner, DirectoryComponent },
  emits: ['dir_clicked'],
  data() {
    return { api_first_page_link: this.get_api_link() }
  },
  watch: {
    current_folder() {
      this.refresh_as_parent_dir_changed()
    },
  },
  methods: {
    get_api_link() {
      return format_url_with_get_params(GAME_FOLDERS_API_LINK, {
        parent_folder: this.current_folder,
      })
    },
    async refresh_as_parent_dir_changed() {
      this.api_first_page_link = this.get_api_link()
      await this.make_api_call()
    },
    on_dir_clicked(dir_id) {
      this.$emit('dir_clicked', dir_id)
    },
  },
  async mounted() {},
}
</script>

<style scoped></style>
