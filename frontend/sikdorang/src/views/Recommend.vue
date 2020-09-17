<template>
  <div>
    <v-btn @click="getRecommend()">식당 추천받기!</v-btn>
    {{ result }}
  </div>
</template>

<script>
export default {
  name: "Recommend",
  data() {
    return {
      userId: null,
      result: null,
    };
  },
  created() {
    this.userId = 744;
  },
  methods: {
    getRecommend() {
      this.$axios
        .get(`/recommend/${this.userId}`)
        .then((response) => {
          this.result = response;
        })
        .catch((error) => {
          console.error(error);
        });
    },
  },
};
</script>

<style>
</style>