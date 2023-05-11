<template>
  <SoundExplorer :is_admin="true" :root_folder_name="'root'" :can_review="true">
  </SoundExplorer>
</template>

<script>
import SoundExplorer from '@/views/sound_sorting/SoundExplorer.vue'

export default {
  name: 'GameSoundExplorerAdmin',
  components: { SoundExplorer },
}
</script>

<style scoped></style>
