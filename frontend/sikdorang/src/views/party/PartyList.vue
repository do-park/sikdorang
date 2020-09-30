<template>
  <div>
    <h1>파티구함</h1>
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
      const requestHeaders = {
        headers: {
          Authorization: `JWT ${this.$cookies.get("auth-token")}`,
        },
      };
      this.$axios
        .get(`/party/list_party`, requestHeaders)
        .then((res) => {
          console.log(res.data);
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