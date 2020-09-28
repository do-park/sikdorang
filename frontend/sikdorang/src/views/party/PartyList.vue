<template>
  <div>
    <h1>파티구함</h1>
    <div v-for="(partyList, index) in getPartyList" :key="index">
      <PartyListItem :partyList="partyList" :index="index" />
    </div>
  </div>
</template>

<script>
import PartyListItem from "@/components/party/PartyListItem.vue";
export default {
  name: "PartyList",
  components: {
    PartyListItem,
  },
  computed: {},
};
</script>

<style>
</style>