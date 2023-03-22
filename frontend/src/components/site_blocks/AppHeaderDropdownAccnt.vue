<template>
  <CDropdown variant="nav-item">
    <CDropdownToggle placement="bottom-end" class="py-0" :caret="false">
      <CIcon icon="cil-user" />
    </CDropdownToggle>
    <CDropdownMenu class="pt-0">
      <CDropdownItem>
        <CIcon icon="cil-lock-locked" />
        <a :href="$router.resolve({ name: 'Logout' }).href">Log out</a>
      </CDropdownItem>
    </CDropdownMenu>
  </CDropdown>
</template>

<script>
export default {
  name: 'AppHeaderDropdownAccnt',
  setup() {
    return {}
  },
}
</script>
