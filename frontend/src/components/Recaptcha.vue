<template>
  <vue-recaptcha
    sitekey="6LfbQfsbAAAAAHSMSz0jtyaZG5hFPRRYkeduVs3X "
    size="normal"
    theme="light"
    @verify="recaptchaVerified"
    @expire="recaptchaExpired"
    @fail="recaptchaFailed"
    ref="vueRecaptcha"
  >
  </vue-recaptcha>
</template>

<script>
import vueRecaptcha from 'vue3-recaptcha2'

export default {
  name: 'Recaptcha',
  emits: ['verified'],
  components: {
    vueRecaptcha,
  },
  data() {
    return {}
  },
  methods: {
    recaptchaVerified(response) {
      this.$emit('verified', response)
    },
    recaptchaExpired() {
      this.$refs.vueRecaptcha.reset()
    },
    recaptchaFailed() {},
  },
}
</script>
