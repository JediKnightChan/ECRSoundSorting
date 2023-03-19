<script>
export default {
  name: 'Logout',
  async created() {
    await this.$store.dispatch('logoutUser')
    await this.$router.push({ name: 'Login' })
  },
}
</script>

<style scoped></style>
