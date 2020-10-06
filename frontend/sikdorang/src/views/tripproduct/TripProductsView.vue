<template>
  <!-- 등록된 여행 상품을 전부 보여줍니다. -->
  <div>
    <div class="row m-0 justify-content-center mb-4">
      <h3 class="text-center my-3 y-line">가이드와 함께해요</h3>
    </div>
    <TripProductList />
  </div>
</template>

<script>
import TripProductList from "@/components/guide/TripProductList.vue";

export default {
  name: "TripProductsView",
  components: {
    TripProductList,
  },
};
</script>

<style scoped>
.y-line {
  border-top: 2px solid crimson;
  border-bottom: 2px solid crimson;
  padding: 0.5rem;
  font-weight: bolder;
}
</style>