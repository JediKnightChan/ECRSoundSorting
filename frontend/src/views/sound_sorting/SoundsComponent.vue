<template>
  <SoundComponent
    v-for="item in original_api_data"
    :key="item.id"
    :item_key="'sound' + item.id"
    :item="item"
    :can_review="can_review"
    :is_admin="is_admin"
    @audio_pseudo_clicked="on_audio_pseudo_clicked"
  ></SoundComponent>
  <CenterSpinner v-if="loading"></CenterSpinner>
</template>

<script>
import SoundComponent from '@/views/sound_sorting/SoundComponent.vue'
import APIListMixin from '@/common/mixins/APIListMixin.vue'
import { GAME_SOUNDS_API_LINK } from '@/common/api_endpoints'
import { format_url_with_get_params } from '@/common/utils'
import CenterSpinner from '@/components/CenterSpinner.vue'

export default {
  name: 'SoundsComponent',
  props: {
    current_folder: {},
    hide_reviewed: {
      type: Boolean,
    },
    can_review: {
      type: Boolean,
    },
    is_admin: {
      type: Boolean,
    },
  },
  mixins: [APIListMixin],
  components: { CenterSpinner, SoundComponent },
  emits: ['audio_pseudo_clicked', 'total_sound_amount_changed'],
  data() {
    return {
      api_first_page_link: this.get_api_link(),
      loading_mode: 'pagination',
    }
  },
  watch: {
    current_folder() {
      this.refresh_as_url_changed()
    },
    hide_reviewed() {
      this.refresh_as_url_changed()
    },
    total_item_count() {
      this.$emit('total_sound_amount_changed', this.total_item_count)
    },
  },
  methods: {
    get_api_link() {
      return format_url_with_get_params(GAME_SOUNDS_API_LINK, {
        parent_folder: this.current_folder,
        hide_reviewed: this.hide_reviewed,
      })
    },
    refresh_as_url_changed() {
      this.original_api_data = []
      this.api_first_page_link = this.get_api_link()
      this.api_next_page_link = null
      this.make_api_call()
    },
    on_audio_pseudo_clicked(v1, v2) {
      this.$emit('audio_pseudo_clicked', v1, v2)
    },
  },
}
</script>

<style scoped></style>
