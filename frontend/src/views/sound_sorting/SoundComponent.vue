<template>
  <CAccordionItem :item-key="this.item_key">
    <CAccordionHeader @click="accordion_clicked">
      <CRow class="me-3" style="min-height: 50px">
        <CCol class="d-flex align-items-center" md="auto" sm="6">
          <audio
            ref="myaudio"
            controls
            :src="item.sound_file"
            style="border-radius: 50px"
            class="resizable-audio"
          ></audio>
        </CCol>
        <CCol md="auto" sm="6" class="d-flex align-items-center mt-md-0 mt-2">
          <span class="ms-3"
            ><a :href="item.gdrive_link" target="_blank">{{
              item.name
            }}</a></span
          >
          <span class="ms-4"
            >{{ sound_likes }} <CIcon icon="cil-thumb-up"
          /></span>
          <span class="ms-3">
            {{ sound_dislikes }} <CIcon icon="cil-thumb-down"
          /></span>
        </CCol>
        <CCol v-if="this.is_admin" md="12" class="mt-2">
          <CRow>
            <CCol v-for="item in top_categories" :key="item.name" md="auto">
              <CButton color="light" class="mt-2">
                {{ item.name }} <CBadge color="danger">{{ item.count }}</CBadge>
              </CButton>
            </CCol>
          </CRow>
        </CCol>
      </CRow>
    </CAccordionHeader>
    <CAccordionBody v-if="can_review">
      <CRow>
        <CCol md="4" class="mt-2 mt-md-0">
          <CFormLabel for="soundCategories">Categories</CFormLabel>
          <multiselect
            v-model="categories_value"
            :options="categories_options"
            label="name"
            track-by="id"
            multiple
          ></multiselect>
        </CCol>
        <CCol md="4" class="mt-2 mt-md-0">
          <CFormLabel for="soundTextDesc"
            >Text description (not recommended)
          </CFormLabel>
          <CFormInput type="text" v-model="text_description"></CFormInput>
        </CCol>
        <CCol md="3" class="mt-2 mt-md-0">
          <label class="mb-2">This audio file is useful</label>
          <br />
          <span>
            <CButton
              type="button"
              :class="
                is_sound_useful === true ? 'btn-success' : 'btn-outline-success'
              "
              @click="thumb_up_clicked"
            >
              <CIcon icon="cil-thumb-up" />
            </CButton>
            <CButton
              type="button"
              :class="
                is_sound_useful === false
                  ? 'btn-danger ms-3'
                  : 'btn-outline-danger ms-3'
              "
              @click="thumb_down_clicked"
            >
              <CIcon icon="cil-thumb-down" />
            </CButton>
          </span>
        </CCol>
        <CCol class="container-fluid mt-4 mt-lg-0">
          <CLink
            v-c-tooltip="{
              content: 'Send review',
              placement: 'left',
            }"
          >
            <CButton
              type="button"
              :class="can_send_answer ? 'btn-outline-success' : 'btn-success'"
              style="width: 100%; height: 100%"
              :disabled="!can_send_answer"
              @click="send_answer"
            >
              <CIcon icon="cil-arrow-right"></CIcon>
            </CButton>
          </CLink>
        </CCol>
      </CRow>
    </CAccordionBody>
  </CAccordionItem>
</template>

<script>
import {
  fetch_api_json,
  GET_GAME_SOUND_DETAILS_API_LINK,
  GET_SOUND_REVIEW_DETAILS_API_LINK,
  SOUND_REVIEWS_API_LINK,
} from '@/common/api_endpoints'
import { format_url_with_get_params } from '@/common/utils'
import Swal from 'sweetalert2'

export default {
  name: 'SoundComponent',
  props: {
    item_key: {
      type: String,
    },
    item: {
      type: Object,
    },
    can_review: {
      type: Boolean,
    },
  },
  emits: ['audio_pseudo_clicked'],
  data() {
    return {
      didnt_play_audio: true,
      accordion_not_shown_before: true,

      previous_answer_id: null,
      categories_value: null,
      categories_options: [],
      text_description: '',
      is_sound_useful: true,

      sound_likes: this.item.likes,
      sound_dislikes: this.item.dislikes,
    }
  },
  computed: {
    can_send_answer() {
      return this.is_sound_useful !== null
    },
  },
  methods: {
    accordion_clicked() {
      if (this.accordion_not_shown_before) {
        this.load_existing_answer()
        this.accordion_not_shown_before = false
      }

      this.$emit('audio_pseudo_clicked', this.$refs.myaudio, this.item_key)
      this.$refs.myaudio.play()
    },
    async load_existing_answer() {
      let res = await fetch_api_json(
        format_url_with_get_params(SOUND_REVIEWS_API_LINK + this.item.id, {
          sound: this.item.id,
        }),
      )
      let data = await res.json()
      let answer = data

      this.text_description = answer.text_review
      this.is_sound_useful = answer.is_useful
      this.previous_answer_id = answer.id

      // Categories
      if (!this.categories_options) {
        await this.update_categories_options()
      }
      this.categories_value = this.categories_options.filter((x) =>
        answer.categories.includes(x.id),
      )
    },
    async get_top_categories() {
      let res = await fetch_api_json(
        GET_GAME_SOUND_DETAILS_API_LINK(this.item.id) +
          'get_suggested_categories/',
        'GET',
      )
      let data = await res.json()
      this.top_categories = data.categories
    },
    async send_answer() {
      let body_data = {
        sound: this.item.id,
        is_useful: this.is_sound_useful,
        categories: this.categories_value
          ? this.categories_value.map((x) => x.id)
          : [],
        text_review: this.text_description,
      }

      let res
      if (
        this.previous_answer_id !== null &&
        this.previous_answer_id !== undefined
      ) {
        res = await fetch_api_json(
          GET_SOUND_REVIEW_DETAILS_API_LINK(this.previous_answer_id),
          'PATCH',
          body_data,
        )
      } else {
        res = await fetch_api_json(SOUND_REVIEWS_API_LINK, 'POST', body_data)
      }

      let data = await res.json()
      if (res.status === 200 || res.status === 201) {
        await Swal.fire({
          position: 'top-end',
          icon: 'success',
          title: `Answer successfly sent`,
          showConfirmButton: false,
          timer: 1000,
        })
      } else {
        await Swal.fire({
          icon: 'error',
          title: `Error`,
          text: JSON.stringify(data),
        })
      }

      if (
        this.previous_answer_id === null ||
        this.previous_answer_id === undefined
      ) {
        this.previous_answer_id = data.id
      }

      await this.update_likes_dislikes_after_answer()
    },
    async update_likes_dislikes_after_answer() {
      let res = await fetch_api_json(
        GET_GAME_SOUND_DETAILS_API_LINK(this.item.id),
      )
      let data = await res.json()
      this.sound_likes = data.likes
      this.sound_dislikes = data.dislikes
    },
    async update_categories_options() {
      this.categories_options = await this.$store.dispatch('retrieveCategories')
    },
    thumb_up_clicked() {
      if (this.is_sound_useful !== true) {
        this.is_sound_useful = true
      }
    },
    thumb_down_clicked() {
      if (this.is_sound_useful !== false) {
        this.is_sound_useful = false
      }
    },
  },
  async mounted() {
    await this.get_top_categories()
    await this.update_categories_options()
  },
}
</script>

<style scoped>
.resizable-audio {
}

@media only screen and (max-width: 600px) {
  .resizable-audio {
    width: 100%;
  }
}
</style>
