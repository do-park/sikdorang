<template>
  <!-- 여행 가이드로 활동할 자격을 신청하는 페이지 -->
  <div>
      <PhoneNumberAuthentication/>
  </div>
</template>

<script>
import PhoneNumberAuthentication from "@/components/authentication/PhoneNumberAuthentication.vue"
export default {
    name: "ApplicationGuideView",
    components: {
        PhoneNumberAuthentication,
    },
    
}
</script>

<style>

</style>