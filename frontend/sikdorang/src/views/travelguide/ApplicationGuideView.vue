<template>
  <!-- 여행 가이드로 활동할 자격을 신청하는 페이지 -->
  <div>
      <PhoneNumberAuthentication @authenticated="authenticated"/>
      <div>대충 약관과 주의사항을 안내하는 공간</div>
      <button @click="onClick()">신청</button>
  </div>
</template>

<script>
import PhoneNumberAuthentication from "@/components/authentication/PhoneNumberAuthentication.vue"

export default {
    name: "ApplicationGuideView",
    components: {
        PhoneNumberAuthentication,
    },
    data() {
        return {
            isAuthenticated: false,
        }
    },
    methods: {
        onClick() {
            if (this.isAuthenticated) {
                const requestHeaders = {
                    headers: {
                        Authorization: `JWT ${this.$cookies.get('auth-token')}`
                    }
                }
                this.$axios.post("guide/apply", null, requestHeaders)
                .then(res => {
                    console.log(res)
                })
                .catch(err => console.error(err))
            }
        },
        authenticated() {
            this.isAuthenticated = true
        }
    }
}
</script>

<style>

</style>