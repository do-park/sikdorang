<template>
  <div class="row mx-3">
    <div class="col-12 p-0" @click="onClick()">
      <div class="m-0 text-truncate custom-title">{{ partyItem.title }}</div>
      <div>
        <small><span class="font-weight-bolder" style="color:crimson;">{{ partyItem.trip_date.toString().substr(0, 4) }}년 {{
              partyItem.trip_date.toString().substr(4, 2)
            }}월 {{ partyItem.trip_date.toString().substr(6, 2) }}일</span>에 같이가요!</small>
        
      </div>
      <!-- <div class="text-right mx-3">{{ partyItem.user.username }}</div> -->
      <hr style="width: 100%" />
    </div>
  </div>
</template>

<script>
import { mapActions } from "vuex";
const party = "party";

export default {
  name: "PartyListItem",
  props: {
    partyItem: Object,
    index: Number,
  },
  data() {
    return {
      trip: Object,
    };
  },
  mounted() {
    this.getTripdata(this.partyItem.id);
  },
  methods: {
    ...mapActions(party, ["actionParty", "actionTrip"]),
    getTripdata(tripId) {
      this.$axios
        .get(`/trip/${tripId}`)
        .then((res) => {
          this.trip = res.data;
        })
        .catch((err) => {
          console.error(err);
        });
    },
    onClick() {
      if (this.$store.state.isLogin) {
        this.actionParty(this.partyItem);
        this.actionTrip(this.trip);
        this.$router.push({ name: "PartyListItemDetail" });
      } else {
        this.$router.push({ name: "Login"});
      }
    },
  },
};
</script>

<style scoped>
.custom-title {
  font-weight: bolder;
}
</style>