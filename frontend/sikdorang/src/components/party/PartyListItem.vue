<template>
  <div class="d-block">
    <div @click="onClick()">
      <h5 class="mx-3">{{ partyItem.title }}</h5>
      <p class="mx-3">날짜: {{ partyItem.trip_date }}</p>
      <p class="text-right mx-3">작성자: {{ partyItem.user.username }}</p>
      <hr style="width: 100%" />
    </div>
  </div>
</template>

<script>
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
    console.log(this.partyItem);
    this.getTripdata(this.partyItem.id);
  },
  methods: {
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
      this.$cookies.set("party", this.partyItem);
      this.$cookies.set("trip", this.trip);
      this.$router.push({ name: "PartyListItemDetail" });
    },
  },
};
</script>

<style>
</style>