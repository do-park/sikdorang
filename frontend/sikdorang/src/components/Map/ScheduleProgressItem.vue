<template>
  <section>
    <div v-if="this.schedule.name[0] == '식'" @click="onClick(index)">
      <i
        :class="[schedule.userChoice ? 'active' : '', 'deactivate']"
        class="fas fa-utensils"
      ></i>
    </div>
    <div v-else-if="this.schedule.name[0] == '카'" @click="onClick(index)">
      <i
        :class="[schedule.userChoice ? 'active' : '', 'deactivate']"
        class="fas fa-coffee"
      ></i>
    </div>
    <div v-else-if="this.schedule.name[0] == '관'" @click="onClick(index)">
      <i
        :class="[schedule.userChoice ? 'active' : '', 'deactivate']"
        class="fas fa-place-of-worship"
      ></i>
    </div>
    <div v-else @click="onClick(index)">
      <i
        :class="[schedule.userChoice ? 'active' : '', 'deactivate']"
        class="fas fa-bed"
      ></i>
    </div>
    <!-- <div
      :class="[schedule.userChoice ? 'active' : '', 'deactivate']"
      @click="onClick(index)"
    >
      {{ schedule.name[0] }}
    </div> -->
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
