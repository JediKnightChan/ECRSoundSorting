<template>
  <slot name="whole_content" v-if="show_all"></slot>
  <div v-else>
    <slot name="truncated_content"></slot>
    <span style="cursor: pointer; font-weight: bold" @click="show_all = true"
      >Ещё...</span
    >
  </div>
</template>

<script>
export default {
  name: 'TruncatedDiv',
  data() {
    return {
      show_all: false,
    }
  },
}
</script>

<style scoped>
span:hover {
  color: #9d114c;
}
</style>
