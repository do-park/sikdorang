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
  data() {
    return {
      partyList: [
        {
          id: 1,
          plan_id: 1,
          user_id: 1,
          updated_at: "2020-09-29",
          content: "여행을 떠나요",
        },
        {
          id: 2,
          plan_id: 2,
          user_id: 1,
          updated_at: "2020-09-30",
          content: "여행을 떠나요",
        },
      ],
    };
  },
};
</script>

<style>
</style>