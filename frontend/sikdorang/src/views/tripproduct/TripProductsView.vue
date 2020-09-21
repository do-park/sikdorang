<template>
    <!-- 등록된 여행 상품을 전부 보여줍니다. -->
    <div>
        <TripProductList/>
    </div>
</template>

<script>
import TripProductList from "@/components/guide/TripProductList.vue"

export default {
    name: "TripProductsView",
    components: {
        TripProductList,
    }
}
</script>

<style>

</style>