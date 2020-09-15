<template>
    <div class="d-flex" @click="onClick">
        <div v-for="tripItem in tripList" :key="tripItem.id">
            <h3>{{ tripItem.title }}</h3>
            <p>{{ tripItem.lat }}</p>
            <p>{{ tripItem.lng }}</p>
        </div>
    </div>
</template>

<script>
import { mapActions } from "vuex"

const mypage = "mypage"

export default {
    name: "TripListItem",
    props: {
        tripList: Array,
        index: Number,
    },
    methods: {
        ...mapActions(mypage, [
            'actionClickedIndex'
        ]),
        onClick() {
            this.actionClickedIndex(this.index)
        }
    }
}
</script>

<style>

</style>