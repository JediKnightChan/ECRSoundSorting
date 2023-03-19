<template>
  <div class="bg-light min-vh-100 d-flex flex-row align-items-center">
    <CContainer>
      <CRow class="justify-content-center">
        <CCol :md="8">
          <CCardGroup>
            <CCard class="p-4">
              <CCardBody>
                <CForm>
                  <h1>Вход</h1>
                  <p class="text-medium-emphasis">Войдите в свой аккаунт</p>
                  <CInputGroup class="mb-3">
                    <CInputGroupText>
                      <CIcon icon="cil-user" />
                    </CInputGroupText>
                    <CFormInput
                      placeholder="Логин"
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
                      placeholder="Пароль"
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
                    >Пожалуйста, введите корректные логин и пароль. Учтите, что
                    они чувствительны к регистру.
                  </CAlert>

                  <CRow>
                    <CCol :xs="6">
                      <CButton
                        type="button"
                        color="primary"
                        class="px-4"
                        :disabled="!login_enabled"
                        @click="login_user"
                        >Войти
                      </CButton>
                    </CCol>
                    <CCol :xs="6" class="text-right">
                      <CButton type="button" color="link" class="px-0">
                        Забыли пароль?
                      </CButton>
                    </CCol>
                  </CRow>
                </CForm>
              </CCardBody>
            </CCard>
            <CCard class="text-white bg-primary py-5" style="width: 44%">
              <CCardBody class="text-center">
                <div>
                  <h2>Регистрация</h2>
                  <p>
                    Lorem ipsum dolor sit amet, consectetur adipisicing elit,
                    sed do eiusmod tempor incididunt ut labore et dolore magna
                    aliqua.
                  </p>
                  <CButton color="light" variant="outline" class="mt-3">
                    Зарегистрироваться
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
      console.log('Verified', this.recaptcha_value)
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
        let redirect_url = this.$router.resolve({ name: 'Blog' }).href
        if (this.$router.currentRoute.value.query.next) {
          redirect_url = '#' + this.$router.currentRoute.value.query.next
        }
        console.log(redirect_url)
        window.location.href = redirect_url
        window.location.reload()
      }
    },
  },
}
</script>
