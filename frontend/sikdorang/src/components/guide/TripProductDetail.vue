<template>
    <div>
        <div>
            <img :src="detail.img" alt="">
        </div>
        <div>
            <h3>[{{ detail.area }}]{{ detail.title }}</h3>
            <span>{{ startDate }} ~ {{ endDate }} 1인 ￦{{ detail.price }}</span>
        </div>
        <div>
            {{ detail.now_person }} / {{ detail.limit_person }}
        </div>
        <div>
            {{ detail.departure_person }}명 이상 신청 시 출발
        </div>
        <div v-if="!finish">
            <button v-if="isLogin" class="btn btn-primary" @click="onClick()">신청하기</button>
            <div v-else>로그인시 신청이 가능합니다.</div>
        </div>
        <div v-else>
            마감되었습니다.
        </div>        
        <hr>
        <viewer v-if="detail.content" :initialValue="detail.content"/>
    </div>
</template>

<script>
import '@toast-ui/editor/dist/toastui-editor-viewer.css'
import { Viewer } from '@toast-ui/vue-editor'
import { mapActions } from 'vuex'

export default {
    name: "TripProductDetail",
    components: {
        viewer: Viewer,
    },
    mounted() {
        // this.$axios.get(`/guide/detail_tour/${this.$route.params.item_pk}`)
        // .then(res => {
        //     console.log(res)
        //     this.detail = res.data[0]
            
        
        // })
        // .catch(err => console.error(err))

        // this.changeDate // 어디에 넣지
    },
    data() {
        return {
            isLogin: this.$store.state.isLogin,
            startDate: '2020-01-01',
            endDate: '2020-01-02',
            finish: false,
            detail: {
                id: 1,
                user: 1,
                title_img: '이미지',
                title: '가을 여행',
                area: '구미',
                start_date: '2020-9-22',
                end_date: '2020-9-26',
                price: 100,
                start_point: '인동 입석',
                start_time: '09:00',
                content: "",
                limit_person: 10,
                departure_person: 5,
                now_person: 2,
            },
        }
    },
    methods: {
        ...mapActions('order', [
            "actionOrderTrip",
        ]),
        changeDate() {
            console.log(this.detail)
            this.start_date = `${this.detail.start_date.split('-')[0]}년 ${this.item.start_date.split('-')[1]}월 ${this.item.start_date.split('-')[2]}일`
            this.end_date = `${this.detail.end_date.split('-')[0]}년 ${this.item.end_date.split('-')[1]}월 ${this.item.end_date.split('-')[2]}일`,
            this.finish = (this.item.limit_person === this.item.now_person)
        },
        onClick() {
            this.actionOrderTrip(this.detail)
            this.$router.push("/trip/order")
        },
    }
}
</script>

<style>

</style>