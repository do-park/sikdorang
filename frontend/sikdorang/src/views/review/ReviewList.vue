<template>
  <div v-if="reviewList">
    <div v-if="reviews.length > 0">
      <div v-for="review in reviews" :key="review.id">
        <ReviewItem class="item" :review="review"/>
      </div>
    </div>
    <div v-else>
      <div class="margin-custom">작성한 리뷰가 없습니다.</div>
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
.margin-custom {
  margin: 0px 5px;
}
.item {
  margin: 1rem 5px;
}
</style>