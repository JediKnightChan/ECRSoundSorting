<template>
  <CCard>
    <CCardBody>
      <h3 class="mb-2">Folder: {{ current_folder_name }}</h3>
      <h5 class="mb-2" v-if="total_sound_amount !== null">
        Sounds amount: {{ total_sound_amount }}
      </h5>

      <div class="mb-2" v-if="can_review">
        <CFormCheck
          label="Don't show sounds reviewed by me"
          v-model="hide_reviewed"
        ></CFormCheck>
      </div>

      <CAccordion ref="accordion">
        <DirectoriesComponent
          v-if="current_folder"
          :current_folder="current_folder"
          :parent_folder="parent_folder"
          @dir_clicked="on_dir_clicked"
        ></DirectoriesComponent>
        <SoundsComponent
          @audio_pseudo_clicked="on_audio_pseudo_clicked"
          @total_sound_amount_changed="on_total_sound_amount_changed"
          v-if="current_folder"
          :current_folder="current_folder"
          :hide_reviewed="hide_reviewed"
          :can_review="can_review"
        ></SoundsComponent>
      </CAccordion>
    </CCardBody>
  </CCard>
</template>

<script>
import DirectoriesComponent from '@/views/sound_sorting/DirectoriesComponent.vue'
import SoundsComponent from '@/views/sound_sorting/SoundsComponent.vue'
import {
  fetch_api_json,
  GAME_FOLDERS_API_LINK,
  GET_GAME_FOLDER_DETAILS_API_LINK,
} from '@/common/api_endpoints'
import { format_url_with_get_params } from '@/common/utils'

export default {
  name: 'SoundExplorer',
  components: { SoundsComponent, DirectoriesComponent },
  props: {
    root_folder_name: {
      type: String,
      default: 'root',
    },
    can_review: {
      type: Boolean,
      default: true,
    },
  },
  data() {
    return {
      root_folder: null,
      current_folder: null,
      current_folder_name: null,
      parent_folder: null,
      latest_audio_el: null,
      hide_reviewed: true,
      total_sound_amount: null,
    }
  },
  methods: {
    async on_dir_clicked(dir_id) {
      let res = await fetch_api_json(GET_GAME_FOLDER_DETAILS_API_LINK(dir_id))
      let data = await res.json()
      this.parent_folder = data.parent_folder
      this.current_folder = dir_id
      this.current_folder_name = data.name

      window.location = this.$router.resolve({
        path: this.$route.path,
        query: { folder: dir_id },
      }).href
    },
    on_audio_pseudo_clicked(audio_el) {
      if (audio_el !== this.latest_audio_el) {
        if (this.latest_audio_el) {
          this.latest_audio_el.pause()
        }
        this.latest_audio_el = audio_el
      }
    },
    on_total_sound_amount_changed(new_amount) {
      this.total_sound_amount = new_amount
    },
  },
  async mounted() {
    let res = await fetch_api_json(
      format_url_with_get_params(GAME_FOLDERS_API_LINK, { is_root_dir: true }),
    )
    let data = await res.json()
    let game_root = data.results.find((x) => x.name === this.root_folder_name)
    this.root_folder = game_root.id

    if (this.$route.query.folder) {
      let folder_id = this.$route.query.folder
      let folder_res = await fetch_api_json(
        GET_GAME_FOLDER_DETAILS_API_LINK(folder_id),
      )
      let data = await folder_res.json()

      this.current_folder = folder_id
      this.parent_folder = data.parent_folder
      this.current_folder_name = data.name
    } else {
      this.current_folder = game_root.id
      this.current_folder_name = game_root.name
    }
  },
}
</script>

<style src="vue-multiselect/dist/vue-multiselect.css"></style>
