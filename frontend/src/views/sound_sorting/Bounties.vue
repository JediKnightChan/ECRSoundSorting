<template>
  <SoundExplorer
    :root_folder_name="'bounties'"
    :can_review="false"
  ></SoundExplorer>
</template>

<script>
import SoundExplorer from '@/views/sound_sorting/SoundExplorer.vue'

export default {
  name: 'Bounties',
  components: { SoundExplorer },
}
</script>

<style scoped></style>
