<template>
  <CRow>
    <CCol md="6" sm="12">
      <CCard>
        <CCardBody>
          <CRow class="my-4">
            <CCol md="9" class="mx-auto">
              <h1>Overview</h1>
              <p class="mt-4">
                Unfortunately, we didn't manage to link sounds to the
                corresponding game events programmatically. While in EC there
                are more than 100 000 sounds, we don't need to sort them all.
              </p>
              <p>
                <b>Most needed sounds are sound effects (SFX)</b>, eg sounds of
                Space Marine footsteps, power sword impact when hitting the
                enemy or plasma gun fire. Presumably, they should be in
                <b>folders with corresponding names</b> (LSM power sword impact
                &mdash; either in SNB_PowerSword_IM or SNB_Weapons_Melee or in a
                folder with similar name), but that's not for sure.
              </p>

              <p>
                Voice-over is also present here (though I didn't include French
                one), but it's lowest priority as it could be possibly sorted by
                AI later.
              </p>

              <p>
                You can find most wanted sound list in the
                <b>Bounties</b> section.
              </p>
            </CCol>
          </CRow>
        </CCardBody>
      </CCard>
    </CCol>
    <CCol md="6" sm="12" class="my-4 my-sm-0">
      <CCard>
        <CCardBody>
          <CRow class="my-4">
            <CCol md="9" class="mx-auto">
              <h1>Instruction</h1>

              <h2 class="mt-4">Scanning mode (recommended)</h2>
              <p class="mt-4">
                For maximum efficiency, this course of action is recommended.
                You should decide what you want to find (eg, some LSM melee
                sounds) and think which folders can be corresponding
                (SNB_PowerSword_IM, SNB_PowerSword_CM, SNB_Weapons_Melee,
                SNB_Common_Astartes, etc.). Then you should start listening to
                the sounds in that folder and:
              </p>

              <p>
                1. If sound seems <b style="color: red">not useful</b> &mdash;
                <b>skip it, don't send a review</b>
                (for more efficiency).
                <br />
                2.1. If sound seems to be
                <b style="color: darkgoldenrod">useful</b>, but you prefer
                quantity over quality,
                <b>just press large green button to the left</b> and a review
                with auto selected "like" will be sent.
                <br />
                2.2. If you think this sound
                <b style="color: darkgreen">is really important</b>,
                <b>fill the categories</b> (eg you found sound of plasma gun
                impact on water, then possible categories are:
                "Weapons.Ranged.Plasma", "Weapons.Ranged.Impact.Water") and then
                send the answer.
              </p>

              <p>
                Note that you don't have to click a small button on the audio
                player to start listening to the sound, as
                <b
                  >when you open the review form, sound is automatically
                  played</b
                >
                and sound from the previous form is automatically paused.
              </p>

              <h2>Slow mode</h2>
              <p class="mt-4">
                Involves the same as above, but also with sending dislikes
                and/or filling out categories everywhere. Even here you
                shouldn't fill text description, do it only if you found a
                voice-over line that is one of the main ones in the game and you
                heard it very often.
              </p></CCol
            >
          </CRow>
        </CCardBody>
      </CCard>
    </CCol>
  </CRow>
</template>

<script>
export default {
  name: 'Main',
}
</script>

<style scoped></style>
