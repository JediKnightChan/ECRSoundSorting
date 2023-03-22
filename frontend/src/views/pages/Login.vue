<template>
  <div class="bg-light min-vh-100 d-flex flex-row align-items-center">
    <CContainer>
      <CRow class="justify-content-center">
        <CCol :md="8">
          <CCardGroup>
            <CCard class="p-4">
              <CCardBody>
                <CForm>
                  <h1>Log In</h1>
                  <p class="text-medium-emphasis">Login into your account</p>
                  <CInputGroup class="mb-3">
                    <CInputGroupText>
                      <CIcon icon="cil-user" />
                    </CInputGroupText>
                    <CFormInput
                      placeholder="Login"
                      autocomplete="username"
                      v-model="username"
                    />
                  </CInputGroup>
                  <CInputGroup class="mb-4">
                    <CInputGroupText>
                      <CIcon icon="cil-lock-locked" />
                    </CInputGroupText>
                    <CFormInput
                      type="password"
                      placeholder="Password"
                      autocomplete="current-password"
                      v-model="password"
                    />
                  </CInputGroup>

                  <Recaptcha
                    ref="recaptcha"
                    @verified="recaptcha_verified"
                  ></Recaptcha>
                  <br />

                  <CAlert color="danger" v-if="wrong_cred"
                    >Please, enter correct username and password. Take into
                    account that lowercase / uppercase is important.
                  </CAlert>

                  <CRow>
                    <CCol :xs="6">
                      <CButton
                        type="button"
                        color="primary"
                        class="px-4"
                        :disabled="!login_enabled"
                        @click="login_user"
                        >Log in
                      </CButton>
                    </CCol>
                    <CCol :xs="6" class="text-right">
                      <CButton type="button" color="link" class="px-0">
                        <a :href="$router.resolve({ name: 'Signup' }).href"
                          >Forgot your password?</a
                        >
                      </CButton>
                    </CCol>
                  </CRow>
                </CForm>
              </CCardBody>
            </CCard>
            <CCard class="text-white bg-primary py-5" style="width: 44%">
              <CCardBody class="text-center">
                <div>
                  <h2>Signup</h2>
                  <p>
                    To participate in the sound sorting for Eternal Crusade:
                    Resurrection, please, register an account, it is required
                    for security reasons. No additional verification for it
                    (like email) is required.
                  </p>
                  <CButton color="light" variant="outline" class="mt-3">
                    <a
                      :href="$router.resolve({ name: 'Signup' }).href"
                      class="no-deco-link"
                      >Sign Up</a
                    >
                  </CButton>
                </div>
              </CCardBody>
            </CCard>
          </CCardGroup>
        </CCol>
      </CRow>
    </CContainer>
  </div>
</template>

<script>
import Recaptcha from '@/components/Recaptcha'

export default {
  name: 'Login',
  components: { Recaptcha },
  data() {
    return {
      username: '',
      password: '',
      recaptcha_value: '',
      wrong_cred: false,
    }
  },
  computed: {
    login_enabled() {
      return this.recaptcha_value && this.username && this.password
    },
  },
  methods: {
    recaptcha_verified(response) {
      this.recaptcha_value = response
    },
    async login_user() {
      this.wrong_cred = false
      this.wrong_cred = await this.$store.dispatch('loginUser', {
        username: this.username,
        password: this.password,
        recaptcha: this.recaptcha_value,
      })
      if (this.wrong_cred) {
        this.$refs.recaptcha.recaptchaExpired()
      } else {
        let redirect_url = this.$router.resolve({ name: 'Main' }).href
        if (this.$router.currentRoute.value.query.next) {
          redirect_url = '#' + this.$router.currentRoute.value.query.next
        }
        window.location.href = redirect_url
        window.location.reload()
      }
    },
  },
}
</script>
