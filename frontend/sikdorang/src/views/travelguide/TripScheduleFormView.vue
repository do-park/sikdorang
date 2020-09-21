<template>
    <!-- 가이드가 일정을 생성하는 페이지 -->
    <div>
        <TripScheduleForm/>
    </div>
</template>

<script>
import TripScheduleForm from "@/components/guide/TripScheduleForm.vue"

export default {
    name: "TripScheduleFormView",
    components: {
        TripScheduleForm,
    },

}
</script>

<style>

</style>