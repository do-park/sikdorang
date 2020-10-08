<template>
  <div class="mx-2">
    <div
      class="item-wrap"
      v-for="item in tripProductList"
      :key="item.id"
      @click="goTripProductDetailPage(item.id)"
    >
      <TripProductItem :item="item" />
    </div>
    <!-- <infinite-loading @infinite="infiniteHandler" spinner="waveDots"></infinite-loading> -->
  </div>
</template>

<script>
import TripProductItem from "./TripProductItem.vue";

export default {
  name: "TripProductList",
  components: {
    TripProductItem,
  },
  data() {
    return {
      // limit: 0,
      tripProductList: [],
      targetGuide: null,
    };
  },
  mounted() {
    this.$axios
      .get(`/guide/list_tour`)
      .then((res) => {
        this.tripProductList = res.data;
      })
      .catch((err) => {
        console.error(err);
      });
  },
  methods: {
    // infiniteHandler($state) {
    //     this.$axios.get(`/trip/${this.limit}`)
    //     .then(res => {
    //         // console.log(res)
    //         setTimeout(()=> {
    //             if (res.data.content.length) {
    //                 this.yogaList = this.tripProductList.concat(res.data.content);
    //                 $state.loaded();
    //                 this.limit += 10
    //                 if (this.tripProductList.length / 10 === 0){
    //                     $state.complete();
    //                 }
    //             } else {
    //                 $state.complete();
    //             }

    //         }, 500)
    //     })
    //     .catch(err => {
    //         console.error(err)
    //     })
    // },

    goTripProductDetailPage(item_pk) {
      this.$router.push(`/trip/detail/${item_pk}`);
    },
    // getThatGuideList() {
    //     this.$axios.get(`/trip/list/${this.targetGuide}`)
    //     .then(res => {
    //         console.log(res)
    //         this.tripProductList = res.data
    //     })
    //     .catch(err => console.log(err))
    // },
  },
};
</script>

<style scoped>
.item-wrap {
  cursor: pointer;
}

</style>