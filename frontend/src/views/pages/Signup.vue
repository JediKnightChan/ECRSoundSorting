<template>
  <div class="bg-light min-vh-100 d-flex flex-row align-items-center">
    <CContainer>
      <CRow class="justify-content-center">
        <CCol :md="6">
          <CCardGroup>
            <CCard class="p-4">
              <CCardBody>
                <CForm>
                  <h1>Signup</h1>
                  <p class="text-medium-emphasis">
                    Register your new account here
                  </p>
                  <CInputGroup class="mb-3">
                    <CInputGroupText>
                      <CIcon icon="cil-user" />
                    </CInputGroupText>
                    <CFormInput
                      placeholder="Username"
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
                      v-model="password"
                    />
                  </CInputGroup>
                  <CInputGroup class="mb-4">
                    <CInputGroupText>
                      <CIcon icon="cil-lock-locked" />
                    </CInputGroupText>
                    <CFormInput
                      type="password"
                      placeholder="Confirm password"
                      v-model="password2"
                    />
                  </CInputGroup>

                  <Recaptcha
                    ref="recaptcha"
                    @verified="recaptcha_verified"
                  ></Recaptcha>
                  <br />

                  <CAlert color="danger" v-if="password !== password2"
                    >Passwords do not match
                  </CAlert>

                  <CRow>
                    <CCol :xs="6">
                      <CButton
                        type="button"
                        color="primary"
                        class="px-4"
                        :disabled="!signup_enabled"
                        @click="signup_user"
                        >Sign Up
                      </CButton>
                    </CCol>
                    <CCol :xs="6">
                      <CButton
                        type="button"
                        color="link"
                        class="px-0 float-end"
                      >
                        <a :href="$router.resolve({ name: 'Login' }).href"
                          >Already have an account?</a
                        >
                      </CButton>
                    </CCol>
                  </CRow>
                </CForm>
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
import { AUTH_SIGNUP_API_LINK, fetch_auth_json } from '@/common/api_endpoints'
import Swal from 'sweetalert2'

export default {
  name: 'Signup',
  components: { Recaptcha },
  data() {
    return {
      username: '',
      password: '',
      password2: '',
      recaptcha_value: '',
    }
  },
  computed: {
    signup_enabled() {
      return (
        this.recaptcha_value &&
        this.username &&
        this.password &&
        this.password === this.password2
      )
    },
  },
  methods: {
    recaptcha_verified(response) {
      this.recaptcha_value = response
    },
    async signup_user() {
      const res = await fetch_auth_json(AUTH_SIGNUP_API_LINK, 'POST', {
        username: this.username,
        password: this.password,
        recaptcha_value: this.recaptcha_value,
      })
      if (res.status === 201) {
        await Swal.fire({
          position: 'top-end',
          icon: 'success',
          title: `User registered successfully. Please, log in now`,
          showConfirmButton: false,
          timer: 2500,
        })
        window.location = this.$router.resolve({ name: 'Login' }).href
      } else {
        this.$refs.recaptcha.recaptchaExpired()
        const data = await res.json()
        await Swal.fire({
          icon: 'error',
          title: `Error occurred`,
          text: JSON.stringify(data),
        })
      }
    },
  },
}
</script>
