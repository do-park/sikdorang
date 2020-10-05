<template>
  <div>
    <h3 class="text-center my-3">동행과 함께 여행 어때요?</h3>
    <hr style="width: 100%" />
    <div v-if="partyList">
      <div v-for="(partyItem, index) in partyList" :key="index">
        <PartyListItem :partyItem="partyItem" :index="index" />
      </div>
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
      partyList: [],
    };
  },
  mounted() {
    this.getPartyList();
  },
  methods: {
    getPartyList() {
      this.$axios
        .get(`/party/list_party`)
        .then((res) => {
          console.log("partylist", res.data);
          this.partyList = res.data;
        })
        .catch((err) => {
          console.error(err);
        });
    },
  },
};
</script>

<style>
</style>