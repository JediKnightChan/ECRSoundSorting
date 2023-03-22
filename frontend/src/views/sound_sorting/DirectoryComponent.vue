<template>
  <CAccordionItem :item-key="this.item_key">
    <CAccordionHeader @click="directory_click">
      <CRow class="me-3 overflow-hidden" style="min-height: 50px">
        <CCol class="d-flex align-items-center mt-2 mt-md-0" xs="auto">
          <CIcon icon="cil-folder"></CIcon>
        </CCol>
        <CCol class="d-flex align-items-center mt-md-0 mt-2 overflow-hidden">
          <span class="ms-0 ms-md-3">{{ folder_name }}</span>
        </CCol>
      </CRow>
    </CAccordionHeader>
  </CAccordionItem>
</template>

<script>
export default {
  name: 'DirectoryComponent',
  emits: ['dir_clicked'],
  props: {
    folder_name: {
      type: String,
    },
    folder_id: {},
    item_key: {
      type: String,
    },
  },
  methods: {
    directory_click() {
      this.$emit('dir_clicked', this.folder_id)
    },
  },
}
</script>

<style scoped></style>
