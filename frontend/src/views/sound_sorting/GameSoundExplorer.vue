<template>
  <SoundExplorer
    :root_folder_name="'root'"
    :can_review="true"
    :is_admin="is_admin"
  ></SoundExplorer>
</template>

<script>
import SoundExplorer from '@/views/sound_sorting/SoundExplorer.vue'

export default {
  name: 'GameSoundExplorer',
  components: { SoundExplorer },
  data() {
    return {
      is_admin: this.$route.query.is_admin === 'true',
    }
  },
}
</script>

<style scoped></style>
