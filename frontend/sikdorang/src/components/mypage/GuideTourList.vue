<template>
    <div>
        <h2>가이드 투어 목록</h2>
        <div v-for="tour in tourList" :key="tour.id">
            <GuideTourListItem :tour="tour" />
        </div>
    </div>
</template>

<script>
import GuideTourListItem from './GuideTourListItem.vue'

export default {
    name: 'GuideTourList',
    components: {
        GuideTourListItem,
    },
    data() {
        return {
            tourList: [
                {id: 1,
                title_img: '이미지',
                title: '가을 여행',
                area: '구미',
                start_date: '2020-9-22',
                end_date: '2020-9-23',
                price: 100,
                },
                {id: 2,
                title_img: '이미지',
                title: '가을 여행2',
                area: '구미',
                start_date: '2020-9-22',
                end_date: '2020-9-23',
                price: 100,
                },
            ],
        }
    },
    mounted() {
        this.getData()
    },
    methods: {
        getData() {
            // auth-token 헤더로 보내서 post로 결제한 가이드 투어 리스트 가져오기
        }
    },

}
</script>

<style>

</style>