<template>
  <div v-if="reviewList">
    <div v-for="review in reviews" :key="review.id">
      <ReviewItem :review="review"/>
    </div>
  </div>
</template>

<script>
import ReviewItem from "../../components/review/ReveiwItem"

export default {
  name: "ReviewList",
  components: {
    ReviewItem,
  },
  props : {
    reviewList : Boolean,
  },
  data() {
    return {
      reviews: [],
    }
  },
  mounted() {
    this.getReviewData()
  },
  methods: {
    getReviewData() {
      const requestHeaders = {
        headers: {
          Authorization: `JWT ${this.$cookies.get("auth-token")}`,
        },
      };
      this.$axios.get(`/review/user_review`, requestHeaders)
        .then(res => {
            console.log(res)
            this.reviews = res.data
        })
        .catch(err => console.error(err))
    },
   
  },
};
</script>

<style scoped>

</style>