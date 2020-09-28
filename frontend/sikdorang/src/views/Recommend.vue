<template>
  <div v-if="result">{{ address }}의<br />{{ result.store_name }}</div>
</template>

<script>
export default {
  name: "Recommend",
  data() {
    return {
      result: null,
      address: null,
    };
  },
  created() {
    this.getRecommend();
  },
  methods: {
    getRecommend() {
      const requestHeaders = {
        headers: {
          Authorization: `JWT ${this.$cookies.get("auth-token")}`,
        },
      };
      this.$axios
        .get("/recommend/coldstart", requestHeaders)
        .then((response) => {
          this.result = response.data;
          const temp = this.result.address.split(" ");
          this.address = temp[0] + " " + temp[1];
        })
        .catch((err) => console.error(err));
    },
  },
};
</script>

<style>
</style>