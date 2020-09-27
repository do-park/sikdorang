<template>
    <div
        :class="[schedule.userChoice ? 'active' : '', 'deactivate' ]"
        @click="onClick(index)"
    >
    {{ schedule.name[0] }}
    </div>
</template>

<script>
import { mapActions } from 'vuex'

export default {
    name: "ScheduleProgressItem",
    props: {
        index: Number,
        schedule: Object,
    },
    methods: {
        ...mapActions('schedule', ['actionscheduleProgressIdx']),
        onClick(idx) {
            console.log('클릭됨', idx, this.schedule)
            this.actionscheduleProgressIdx(idx)
        }
    }
}
</script>

<style scoped>
div {
    width: 20px;
    height: 20px;
}
.active {
    background-color: crimson !important;
}
.deactivate {
    background-color: skyblue;
}
</style>