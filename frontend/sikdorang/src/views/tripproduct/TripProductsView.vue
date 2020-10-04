<template>
  <!-- 등록된 여행 상품을 전부 보여줍니다. -->
  <div>
    <h3 class="text-center my-3">여행 상품을 만나보세요!</h3>
    <hr style="width: 100%" />
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

<style>
</style>