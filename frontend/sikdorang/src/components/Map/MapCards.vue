<template>
  <div>
    {{getSchedules}}
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
            data-toggle="modal"
            data-target="#exampleModal"
          >
            A.{{getThreeRes[0].title}}
            <p>@ 맛집 정보 @</p>
          </div>
        </transition>
        <transition enter-active-class="animated flipInY">
          <div
            :class="{ 'active': isActive1 }"
            v-if="animatechk"
            class="box"
            @click="selectRest(1)"
            data-toggle="modal"
            data-target="#exampleModal"
          >
            B.{{getThreeRes[1].title}}
            <p>@ 맛집 정보 @</p>
          </div>
        </transition>
        <transition enter-active-class="animated flipInY">
          <div
            :class="{ 'active': isActive2 }"
            v-if="animatechk"
            class="box"
            @click="selectRest(2)"
            data-toggle="modal"
            data-target="#exampleModal"
          >
            C.{{getThreeRes[2].title}}
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
      recommendations: [],
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
      if ( this.getClicked) {
        this.actionSelectedRest(this.getThreeRes[this.getClicked]);
        this.selectRest(this.getClicked);
      }
    },
    getSchedules() {
      console.log(this.getSchedules)
    }
  },
  mounted() {
    this.fillPositions();
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
          title: Rest.title,
          text: "이런이런 맛집입니다아",
          buttons: ["닫기", "추가"],
        }).then((res) => {
          if (res) {
            swal(`${Rest.title}을 일정에 추가할까요?`, {
              buttons: ["아니오", "네"],
            }).then((res) => {
              if (res) {
                swal(`${Rest.title}을 일정에 추가했습니다`, {
                  icon: "success",
                });
                plans.push(this.getSelectedRest);
                this.actionPlanList(plans);
                console.log("getSchedules!!!!!",this.getSchedules)
                this.actionStore(Rest)
                console.log(">>>>>>",this.getScheduleIdx, typeof(this.getScheduleIdx))
                this.actionScheduleIdx(this.getScheduleIdx+1)
                console.log("getSchedules",this.getSchedules)
                console.log("일정", this.getPlanList);
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
    fillPositions() {
      this.recommendations = [
        {
          id: 1,
          title: "승희 위치",
          latitude: 36.1406514,
          longitude: 128.3271104,
        },
        {
          id: 2,
          title: "인영이집",
          latitude: 36.1035992,
          longitude: 128.4162945,
        },
        {
          id: 3,
          title: "규성집",
          latitude: 36.0954328,
          longitude: 128.3963511,
        },
        {
          id: 4,
          title: "성수집근처쨈나",
          latitude: 36.1115959,
          longitude: 128.4303873,
        },
        {
          id: 5,
          title: "도희동아백화점",
          latitude: 36.119735,
          longitude: 128.3463003,
        },
        {
          id: 6,
          title: "인동스타벅스",
          latitude: 36.1073795,
          longitude: 128.4174558,
        },
      ];
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