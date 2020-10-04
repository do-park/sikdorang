<template>
  <section>
    <div v-if="this.schedule.name[0] == '식'" @click="onClick(index)">
      <i
        :class="[schedule.userChoice ? 'active' : '', 'deactivate']"
        class="fas fa-utensils fa-2x pl-1"
      ></i>
    </div>
    <div v-else-if="this.schedule.name[0] == '카'" @click="onClick(index)">
      <i
        :class="[schedule.userChoice ? 'active' : '', 'deactivate']"
        class="fas fa-coffee fa-2x"
      ></i>
    </div>
    <div v-else-if="this.schedule.name[0] == '관'" @click="onClick(index)">
      <i
        :class="[schedule.userChoice ? 'active' : '', 'deactivate']"
        class="fas fa-place-of-worship fa-2x"
      ></i>
    </div>
    <div v-else @click="onClick(index)">
      <i
        :class="[schedule.userChoice ? 'active' : '', 'deactivate']"
        class="fas fa-bed fa-2x"
      ></i>
    </div>
  </section>
</template>

<script>
import { mapActions } from "vuex";

export default {
  name: "ScheduleProgressItem",
  props: {
    index: Number,
    schedule: Object,
  },
  methods: {
    ...mapActions("schedule", ["actionscheduleProgressIdx"]),
    onClick(idx) {
      this.actionscheduleProgressIdx(idx);
    },
  },
};
</script>

<style scoped>
.active {
  color: crimson !important;
}
.deactivate {
  color: skyblue;
}
</style>
