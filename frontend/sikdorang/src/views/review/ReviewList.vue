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
      reviews: [{
        id: 1,
        content: 'fdfdd',
        score: 3,
        store: 1,
        created_at: '2020-09-20',
        updated_at: '2020-09-21',
        user: 1
      },
      {
        id: 2,
        content: '두번째리뷰~~~',
        score: 4,
        store: 2,
        created_at: '2020-09-24',
        updated_at: '2020-09-25',
        user: 1
      },],
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