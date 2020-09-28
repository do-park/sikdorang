<template>
  <div class="d-flex">
    <div>
      {{ partyItem }}
    </div>
  </div>
</template>

<script>
export default {
  name: "PartyListItem",
  props: {
    partyItem: Array,
    index: Number,
  },
};
</script>

<style>
</style>