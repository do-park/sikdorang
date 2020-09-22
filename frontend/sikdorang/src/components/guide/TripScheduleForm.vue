<template>
    <div>
        <label for="title">제목</label>
        <input type="text" id="title" v-model="title">
        <br>
        <label for="t-i">대표이미지</label><br>
        <input
            type="file"
            ref="tI"
            id="t-i"
            accept=".jpg, .jpeg, .gif, .png"
        />
        <br>
        <label for="area">지역</label>
        <!-- Area 도 - 시/군/구 선택 -->
        <input type="text" id="area" v-model="area">
        <br>

        <!-- 시작 날짜 - 종료 날짜 -->
        <label for="start_date">시작일</label>
        <input type="text" id="start_date" v-model="start_date">
        <br>
        <label for="end_date">종료일</label>
        <input type="text" id="end_date" v-model="end_date">
        <br>

        <label for="price">가격</label>
        <input type="text" id="price" v-model="price"/>
        <br>

        <label for="time">출발시간</label>
        <input type="text" id="time" v-model="start_time">
        <br>
        <label for="start_point">출발장소</label>
        <!-- 주소검색 -->
        <input type="text" id="start_point" v-model="start_point">
        <br>
        <editor class="editor"
            :initialValue="editorText"
            ref="toastuiEditor"
            height="500px"
            initialEditType="wysiwyg"
            previewStyle="vertical"
        />
        <button @click="onClick()">생성</button>
    </div>
</template>

<script>
import 'codemirror/lib/codemirror.css'
import '@toast-ui/editor/dist/toastui-editor.css'

import { Editor } from '@toast-ui/vue-editor'

// const FirstArea = [
//     "서울", "부산", "인천", "대구", "광주", "대전", "울산", "강원", "경기", "경남", "경북", "전남", "전북", "충남", "충북", "제주"
// ]
export default {
    name: "TripScheduleForm",
    components: {
        editor: Editor,
    },
    data() {
        return {
            title: null,
            area: null,
            start_date: null,
            end_date: null,
            price: null,
            start_time: null,
            start_point: null,
            editorText: '여행 일정에 대한 자세한 설명을 추가해주세요.',
            content: null,
            editorOptions: {
                hideModeSwitch: true
            },
        }
    },
    methods: {
        onClick() {
            console.log(this.tripSchedule)
            const requestHeaders = {
				headers: {
					Authorization: `JWT ${this.$cookies.get('auth-token')}`
				}
			}
            console.log(requestHeaders)
            let fd = new FormData()
            let image = this.$refs.tI.files[0]
            fd.append('title_img', image)
            fd.append('title', this.title)
            fd.append('area', this.area)
            fd.append('start_date', this.start_date)
            fd.append('end_date', this.end_date)
            fd.append('price', this.price)
            fd.append('start_point', this.start_point)
            fd.append('start_time', this.start_time)
            fd.append('content', this.content)
            console.log(fd)
			this.$axios.post('guide/', fd, requestHeaders)
			.then(res => {
                console.log(res)
                // 등록이 완료되면 리턴되는 객체에서 id 값을 이용해 push한다.
                this.$router.push(`/trip/detail/${res.data.id}`)
			})
			.catch(err => console.error(err))
        },
        getHtml() {
            let html = this.$refs.toastuiEditor.invoke('getHtml')
            this.content = html
        },

    }
}
</script>

<style>

</style>