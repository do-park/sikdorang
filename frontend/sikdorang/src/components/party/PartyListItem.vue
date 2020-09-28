<template>
  <div class="d-flex" @click="onClick">
    <div v-for="partyItem in partyList" :key="partyItem.id">
      <h3>{{ partyItem.title }}</h3>
      <p>{{ partyItem.lat }}</p>
      <p>{{ partyItem.lng }}</p>
    </div>
  </div>
</template>

<script>
export default {
  name: "PartyListItem",
  props: {
    partyList: Array,
    index: Number,
  },
};
</script>

<style>
</style>