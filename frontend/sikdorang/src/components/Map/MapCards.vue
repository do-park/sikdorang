<template>
  <div v-if="threeRes">
    <div class="d-flex flex-column align-items-center">
      <div>
        <button class="btn btn-secondary" @click="checkFilp">
          {{ buttonStr }}
        </button>
      </div>

      <div class="d-flex justify-content-center">
        <transition
          v-for="(res, idx) in threeRes"
          :key="res.id"
          enter-active-class="animated flipInY"
        >
          <div
            :class="{ active: isActive(idx) }"
            v-if="animatechk"
            class="box"
            @click="selectRest(idx)"
            @mouseover="actionMouseOver(idx)"
            @mouseleave="actionMouseOver(null)"
          >
            {{ index[idx] }}.{{ res.name }}
            <p>@ 맛집 정보 @</p>
          </div>
        </transition>
        <br />
      </div>
    </div>
  </div>
</template>

<script>
import Swal from "sweetalert2";
import { mapGetters, mapActions } from "vuex";
const mapEvent = "mapEvent";

export default {
  name: "MapCards",
  data() {
    return {
      plans: this.getPlanList,
      threeRes: this.getThreeRes,
      isActive0: false,
      isActive1: false,
      isActive2: false,
      animatechk: true,
      index: ["A", "B", "C"],
      buttonStr: null,
    };
  },
  props: {
    kakao: Object,
  },
  computed: {
    ...mapGetters(mapEvent, [
      "getFlip",
      "getmouseOverToCard",
      "getClicked",
      "getThreeRes",
      "getSelectedRest",
      "getPlanList",
      "getTagStores",
    ]),
    ...mapGetters("schedule", ["getSchedules", "getScheduleIdx"]),
  },
  watch: {
    getmouseOverToCard() {
      this.changeOverBox(this.getmouseOverToCard);
    },
    getClicked() {
      if (this.getClicked !== null) {
        this.actionSelectedRest(this.getThreeRes[this.getClicked]);
        this.selectRest(this.getClicked);
      }
    },
    getThreeRes() {
      if (this.getThreeRes.length !== 0) {
        this.threeRes = this.getThreeRes;
      }
    },
    getTagStores() {
      if (this.getTagStores) {
        this.buttonStr = "추천해주세요!";
      } else {
        this.buttonStr = `다른 ${
          this.getSchedules[this.getScheduleIdx].name
        } 볼래요!`;
      }
    },
    getScheduleIdx() {
      if (this.getScheduleIdx && this.getTagStores) {
        this.buttonStr = "추천해주세요!";
      } else {
        this.buttonStr = `다른 ${
          this.getSchedules[this.getScheduleIdx].name
        } 볼래요!`;
      }
    },
  },
  mounted() {
    // this.checkFilp();
    if (this.getThreeRes) {
      this.actionSelectedRest(this.getThreeRes[0]);
    }
    if (this.getTagStores) {
      this.buttonStr = "추천해주세요!";
    } else {
      this.buttonStr = `다른 ${
        this.getSchedules[this.getScheduleIdx].name
      } 볼래요!`;
    }
  },
  methods: {
    ...mapActions(mapEvent, [
      "actionFlip",
      "actionSelectedRest",
      "actionClicked",
      "actionPlanList",
      "actionMouseOver",
      "actionTagStores",
      "actionSelectTag",
    ]),
    ...mapActions("schedule", ["actionStore", "actionScheduleIdx"]),

    selectRest(idx) {
      this.actionClicked(idx);
      var plans = this.getPlanList;
      if (this.getTagStores) {
        this.actionSelectedRest(this.getTagStores[idx]);
      } else {
        this.actionSelectedRest(this.getThreeRes[idx]);
      }
      var Rest = this.getSelectedRest;
      Swal.fire({
        title: Rest.name,
        text: Rest.tel,
        showCancelButton: true,
        confirmButtonText: "일정 추가",
        cancelButtonText: "취소",
      }).then((res) => {
        if (res.isConfirmed) {
          Swal.fire({
            icon: "success",
            title: `${Rest.name}을 일정에 추가했습니다`,
          });
          plans.push(this.getSelectedRest);
          this.actionTagStores(false);
          this.actionPlanList(plans);
          this.actionStore(Rest);
          this.actionSelectTag(null);
          this.actionScheduleIdx(this.getScheduleIdx + 1);
        } else {
          this.actionClicked(null);
        }
      });
    },
    isActive(idx) {
      if (this.isActive0 && idx === 0) {
        return true;
      } else if (this.isActive1 && idx === 1) {
        return true;
      } else if (this.isActive2 && idx === 2) {
        return true;
      } else {
        return false;
      }
    },
    changeOverBox(overidx) {
      this.isActive0 = false;
      this.isActive1 = false;
      this.isActive2 = false;

      if (overidx === 0) {
        this.isActive0 = true;
      } else if (overidx === 1) {
        this.isActive1 = true;
      } else if (overidx === 2) {
        this.isActive2 = true;
      } else {
        this.isActive0 = false;
        this.isActive1 = false;
        this.isActive2 = false;
      }
    },
    checkFilp() {
      this.actionFlip(!this.getFlip);
      this.actionTagStores(false);
      this.actionSelectTag(null);
      // this.actionClicked(null);
      this.animatechk = false;
      setTimeout(() => {
        this.animatechk = true;
      }, 100);
    },
  },
};
</script>

<style scoped>
@import "https://cdn.jsdelivr.net/npm/animate.css@3.5.1";
.box {
  margin: 2px;
  text-align: center;
  background-color: lightgray;
  width: 130px;
}
.box:hover {
  cursor: pointer;
  background-color: lightblue;
}
.active {
  cursor: pointer;
  background-color: lightblue;
}
</style>