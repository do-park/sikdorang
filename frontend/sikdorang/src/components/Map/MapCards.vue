<template>
  <div>
    <div class="d-flex flex-column align-items-center">
      <div>
        <button class="btn btn-secondary" @click="checkFilp">다른거 볼래요</button>
      </div>
    
      <div class="d-flex justify-content-center">
        <transition enter-active-class="animated flipInY">
          <div
            :class="{ 'active': isActive0 }"
            v-if="animatechk"
            class="box"
            @click="selectRest(0)"
          >
            A.{{getThreeRes[0].name}}
            <p>@ 맛집 정보 @</p>
          </div>
        </transition>
        <transition enter-active-class="animated flipInY">
          <div
            :class="{ 'active': isActive1 }"
            v-if="animatechk"
            class="box"
            @click="selectRest(1)"
          >
            B.{{getThreeRes[1].name}}
            <p>@ 맛집 정보 @</p>
          </div>
        </transition>
        <transition enter-active-class="animated flipInY">
          <div
            :class="{ 'active': isActive2 }"
            v-if="animatechk"
            class="box"
            @click="selectRest(2)"
          >
            C.{{getThreeRes[2].name}}
            <p>@ 맛집 정보 @</p>
          </div>
        </transition>
        <br />
      </div>
    </div>
  </div>
</template>

<script>
import swal from "sweetalert";
import { mapGetters, mapActions } from "vuex";
const mapEvent = "mapEvent";

export default {
  name: "MapCards",
  data() {
    return {
      plans: this.getPlanList,

      isActive0: false,
      isActive1: false,
      isActive2: false,
      animatechk: true,
    };
  },
  props: {
    kakao: Object,
  },
  computed: {
    ...mapGetters(mapEvent, [
      "getFlip",
      "getMouseOver",
      "getClicked",
      "getThreeRes",
      "getSelectedRest",
      "getPlanList",
    ]),
    ...mapGetters("schedule",[
      "getSchedules",
      "getScheduleIdx",
    ])
  },


  watch: {
    getMouseOver() {
      this.changeOverBox(this.getMouseOver);
    },
    getClicked() {
      if ( this.getClicked !== null ) {
        this.actionSelectedRest(this.getThreeRes[this.getClicked]);
        this.selectRest(this.getClicked);
      }
      
    },
  },
  mounted() {
   
    this.checkFilp();
    if (this.getThreeRes) {
      this.actionSelectedRest(this.getThreeRes[0]);
    }
  },
  methods: {
    ...mapActions(mapEvent, [
      "actionFlip",
      "actionSelectedRest",
      "actionClicked",
      "actionPlanList",
    ]),
    ...mapActions("schedule",[
      "actionStore",
      "actionScheduleIdx"
    ]),

    selectRest(idx) {
      var plans = this.getPlanList;
      if (idx < 3 && idx >= 0) {
        this.actionClicked(idx);
        this.actionSelectedRest(this.getThreeRes[idx]);
        var Rest = this.getSelectedRest;
        swal({
          title: Rest.name,
          text: "이런이런 맛집입니다아",
          buttons: ["닫기", "추가"],
        }).then((res) => {
          if (res) {
            swal(`${Rest.name}을 일정에 추가할까요?`, {
              buttons: ["아니오", "네"],
            }).then((res) => {
              if (res) {
                swal(`${Rest.name}을 일정에 추가했습니다`, {
                  icon: "success",
                });
                plans.push(this.getSelectedRest);
                this.actionPlanList(plans);
                this.actionStore(Rest)
                this.actionScheduleIdx(this.getScheduleIdx+1)
              
              }
            });
          }
        });
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
      this.actionClicked(null);
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