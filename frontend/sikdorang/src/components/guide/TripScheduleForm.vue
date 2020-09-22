<template>
    <div>
        <div>
            <label for="t-i">대표이미지</label><br>
            <input
                @change="fileChange"
                type="file"
                ref="tI"
                id="t-i"
                accept=".jpg, .jpeg, .gif, .png" />
        </div>
        <div>
            <label for="area">지역</label>
            <!-- Area 도 - 시/군/구 선택 -->
        </div>
        <div>
            <label for="start_date">시작일</label>
            <input type="date" name="start_date" id="start_date" v-model="tripSchedule.startDate">
        </div>
        <div>
            <label for="end_date">종료일</label>
            <input type="date" name="end_date" id="end_date" v-model="tripSchedule.endDate">
        </div>
        <div>
            <label for="price">가격</label>
            <input class="form-control d-inline-block" type="number" id="price" v-model="tripSchedule.price"/>원
        </div>
        <div>
            <label for="time">출발시간</label>
            <input type="time" name="time" id="time" v-model="tripSchedule.time">
        </div>
        <div>
            <label for="start_point">출발장소</label>
            <input class="form-control" type="text" id="start_point" v-model="tripSchedule.startPoint">
        </div>
        <editor
            v-model="tripSchedule.editorText"
            ref="toastuiEditor"
            :initialValue="tripSchedule.editorText"
            :options="editorOptions"
            height="500px"
            initialEditType="wysiwyg"
            previewStyle="vertical"
        />
        <button class="btn btn-primary" @click="onClick()">생성</button>
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
                image: null,
                imageUrl: null,
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
            this.getHtml()
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
                // 등록이 완료되면 리턴되는 객체에서 id 값을 이용해 push한다.
                // this.$router.push(`/trip/detail/${res.data.id}`)
			})
			.catch(err => console.error(err))
        },
        getHtml() {
            console.log(this.$refs)
            let html = this.$refs.toastuiEditor.invoke('getHtml')
            this.tripSchedule.editorText = html
        },
        fileChange(e) {
            console.log("!!", e)
            var file = e.target.files[0]
            if (file && file.type.match(/^image\/(png|jpeg)$/)) {
                this.tripSchedule.imageUrl = window.URL.createObjectURL(file)
            }
            this.tripSchedule.image = this.$refs.tI.files[0]
        },


    }
}
</script>

<style>

</style>