<template>
    <div v-if="tripList">
        <h1>일정목록</h1>
        <div v-for="(tripList, index) in getTripList" :key="index">
            <TripListItem :tripList="tripList" :index="index"/>
        </div>
    </div>
</template>

<script>
import { mapGetters } from "vuex"
import TripListItem from './TripListItem.vue'

const mypage = "mypage"

export default {
    name: 'TripList',
    components: {
        TripListItem,
    },
    props : {
        tripList : Boolean,
    },

    computed: {
        ...mapGetters(mypage, [
            'getTripList'
        ])
    }

}
</script>

<style>

</style>