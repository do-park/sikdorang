<template>
  <div class="d-flex">
    <div @click="onClick()">
      <h5>{{ partyItem.title }}</h5>
      날짜: {{ partyItem.trip_date }} 작성자: {{ partyItem.user.username }}
      <hr />
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