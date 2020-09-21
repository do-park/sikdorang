<template>
    <div>
        <div v-for="item in tripProductList" :key="item.id">
            <TripProductItme :item="item"/>
        </div>
    </div>
</template>

<script>
import TripProductItem from "./TripProductItem.vue"

export default {
    name: "TripProductList",
    components: {
        TripProductItem,
    },
    data() {
        return {
            index: 1,
            tripProductList: [],
        }
    },
    mounted() {
        axios.get(`/trip/list/${this.index}`)
        .then(res => {
            console.log(res)
        })
        .catch(err => console.error(err))
    },
}
</script>

<style>

</style>