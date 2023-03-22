<template>
  <CContainer>
    <CRow class="p-4">
      <CCol class="d-flex justify-content-center">
        <circles-to-rhombuses-spinner
          :animation-duration="1500"
          :size="40"
          color="#3c4b64"
        />
      </CCol>
    </CRow>
  </CContainer>
</template>

<script>
export default {
  name: 'CenterSpinner',
}
</script>

<style scoped></style>
