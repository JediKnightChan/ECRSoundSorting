<template>
  <SoundExplorer :root_folder_name="'root'" :can_review="true"></SoundExplorer>
</template>

<script>
import SoundExplorer from '@/views/sound_sorting/SoundExplorer.vue'

export default {
  name: 'GameSoundExplorer',
  components: { SoundExplorer },
}
</script>

<style scoped></style>
