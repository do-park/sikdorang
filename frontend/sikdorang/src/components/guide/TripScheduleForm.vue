<template>
    <div>
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
        <br>

        <label for="start_date">시작일</label>
        <label for="end_date">종료일</label>
        <!-- 시작 날짜 - 종료 날짜 -->
        <br>
        <label for="price">가격</label>
        <input type="text" id="price"/>
        <br>

        <label for="time">출발시간</label>
        <input type="text" id="time">
        <br>
        <label for="start_point">출발장소</label>
        <!-- 주소검색 -->
        <input type="text" id="start_point">
        <br>
        <editor
            :initialValue="tripSchedule.editorText"
            :options="editorOptions"
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
            tripSchedule: {
                title: null,
                area: null,
                startDate: null,
                endDate: null,
                price: null,
                time: null,
                startPoint: null,
                editorText: '여행 일정에 대한 자세한 설명을 추가해주세요.',
            },
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
			this.$axios.post('trip/itemcreate', this.tripSchedule, requestHeaders)
			.then(res => {
				console.log(res)
			})
			.catch(err => console.error(err))
        }
    }
}
</script>

<style>

</style>