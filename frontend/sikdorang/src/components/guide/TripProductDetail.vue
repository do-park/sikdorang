<template>
    <div>
        <div>
            <img :src="detail.img" alt="">
        </div>
        <div>
            <h3>{{ detail.title }}</h3>
            <span>{{ detail.startDate }} ~ {{ detail.endDate }} 인당 / {{ detail.price }}</span>
        </div>
        <button @click="onClick()">신청하기</button>
        <hr>
        <viewer/>
    </div>
</template>

<script>
import '@toast-ui/editor/dist/toastui-editor-viewer.css'

import { Viewer } from '@toast-ui/vue-editor'

export default {
    name: "TripProductDetail",
    components: {
        viewer: Viewer,
    },
    mounted() {
        this.$axios.get(`trip/detail/${this.$route.params.item_pk}`)
        .then(res => {
            console.log(res)
        })
        .catch(err => console.error(err))
    },
    data() {
        return {
            detail: null,
        }
    }
}
</script>

<style>

</style>