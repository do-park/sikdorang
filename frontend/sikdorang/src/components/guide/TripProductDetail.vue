<template>
    <div>
        <div>
            <img :src="detail.img" alt="">
        </div>
        <div>
            <h3>{{ detail.title }}</h3>
            <span>{{ detail.start_date.substr(0,10) }} ~ {{ detail.end_date.substr(0,10) }} 1인 ￦{{ detail.price }}</span>
        </div>
        <button v-if="isLogin" class="btn btn-primary" @click="onClick()">신청하기</button>
        <div v-else>로그인시 신청이 가능합니다.</div>
        <hr>
        <viewer v-if="detail.content !== null" :initialValue="detail.content"/>
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
        // this.$axios.get(`trip/detail/${this.$route.params.item_pk}`)
        // .then(res => {
        //     console.log(res)
        // })
        // .catch(err => console.error(err))
    },
    data() {
        return {
            isLogin: this.$store.state.isLogin,
            detail: {
                id: 1,
                user: 1,
                title_img: '이미지',
                title: '가을 여행',
                area: '구미',
                start_date: Date(2020-9-22),
                end_date: Date(2020-9-26),
                price: 100,
                start_point: '인동 입석',
                start_time: '09:00',
                content: '내용내용내용내용내용내용내용내용내용내용내용내용내용내용내용내용내용내용내용내용내용내용내용내용내용내용내용내용'
            },
        }
    },
    methods: {
        ...mapActions('order', [
            "actionOrderTrip",
        ]),
        onClick() {
            this.actionOrderTrip(this.detail)
            this.$router.push("/trip/order")
        },
    }
}
</script>

<style>

</style>