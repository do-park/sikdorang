<template>
  <div class="m-3">
    <h4 class="mt-1 text-center text-truncate">{{ scheduleName }}</h4>
    <div class="text-right schedule-date">
      {{ scheduleDate.toString().substr(0, 4) }}년 {{
        scheduleDate.toString().substr(4, 2)
      }}월 {{ scheduleDate.toString().substr(6, 2) }}일 일정입니다.
    </div>
    <div class="text-right schedule-date" v-if="getIsSik">
      {{ getForUser.store_name }}에서 일정을 시작합니다.
    </div>
    <draggable v-model="clonedItems" :options="clonedItemOptions" class="board">
      <v-btn
        v-for="(item, index) in clonedItems"
        :key="index"
        @click="deleteItem(index)"
        @touchend="deleteItem(index)"
        class="clickable my-2 mx-auto d-block clickable-btn"
      >
        <i v-if="item.id == 'R'" class="fas fa-utensils" style="color: tomato">
          {{ item.name }}</i
        >
        <i v-if="item.id == 'C'" class="fas fa-coffee" style="color: sienna">
          {{ item.name }}</i
        >
        <i
          v-if="item.id == 'S'"
          class="fas fa-place-of-worship"
          style="color: steelblue"
        >
          {{ item.name }}</i
        >
        <i v-if="item.id == 'A'" class="fas fa-bed" style="color: seagreen">
          {{ item.name }}</i
        >
      </v-btn>
    </draggable>

    <p class="text-right mt-0 schedule-small">
      *아이콘을 드래그해 일정을 구성해보세요. 클릭하면 삭제됩니다.
    </p>
    <draggable
      v-model="availableItems"
      :options="availableItemOptions"
      :clone="handleClone"
      class="d-flex justify-content-around"
      style="width: 100%"
    >
      <button
        v-for="(item, index) in availableItems"
        :key="index"
        class="availableItem"
      >
        <div v-if="item.id == 'R'" class="r-border row">
          <i class="fas fa-utensils fa-2x mx-auto align-self-center" style="color: tomato"></i>
        </div>
        <div v-if="item.id == 'C'" class="c-border row">
          <i class="fas fa-coffee fa-2x mx-auto align-self-center" style="color: sienna"></i>
        </div>
        <div v-if="item.id == 'S'" class="s-border row">
          <i class="fas fa-place-of-worship fa-2x mx-auto align-self-center" style="color: steelblue"></i>
        </div>
        <div v-if="item.id == 'A'" class="a-border row">
          <i class="fas fa-bed fa-2x text-center mx-auto align-self-center" style="color: seagreen"></i>
        </div>
        
      </button>
    </draggable>


    <div class="row mx-0 my-2 justify-content-center">
      <button class="col-6 btn btn-danger" @click="createTrip()">다음 ></button>
    </div>
    <br />
  </div>
</template>

<script>
import draggable from "vuedraggable";
import Swal from "sweetalert2";
import { mapActions, mapGetters } from "vuex";

export default {
  name: "Schedule",
  order: 2,
  components: {
    draggable,
  },
  computed: {
    ...mapGetters("sikRec", ["getIsSik", "getForUser"]),
    ...mapGetters("schedule", ["getScheduleDate"]),
  },
  data() {
    return {
      userId: null,
      forUser: null,
      isSik: null,
      scheduleName: null,
      scheduleDate: null,
      // for test
      saved: [],
      clonedItems: [],
      availableItems: [
        {
          name: "식당",
          id: "R",
          userChoice: null,
        },
        {
          name: "카페",
          id: "C",
          userChoice: null,
        },
        {
          name: "관광지",
          id: "S",
          userChoice: null,
        },
        {
          name: "숙박",
          id: "A",
          userChoice: null,
        },
      ],
      clonedItemOptions: {
        group: "items",
      },
      availableItemOptions: {
        group: {
          name: "items",
          pull: "clone",
          put: false,
        },
        sort: false,
      },
    };
  },
  created() {},
  mounted() {
    this.resetScheduleStoreInfo();
    this.createTripStarter();
  },
  methods: {
    ...mapActions("schedule", [
      "actionSchedule",
      "actionScheduleIdx",
      "actionScheduleName",
      "actionScheduleDate",
      "actionClearBeforeCat",
    ]),
    ...mapActions("mapEvent", ["actionFlip", "actionMapEventClear"]),
    createTripStarter() {
      // const self = this
      // const inputValue = new Date().toISOString().substring(0, 10);
      let inputValue = new Date()
        .toLocaleString({
          timeZone: "Asia/Seoul",
        })
        .substring(0, 12);
      inputValue = this.datetostring(inputValue);

      Swal.mixin({
        confirmButtonText: "Next &rarr;",
        showCancelButton: true,
        progressSteps: ["1", "2"],
      })
        .queue([
          {
            icon: "info",
            title: "일정의 이름을 입력하세요.",
            input: "text",
            allowOutsideClick: false,
            inputValue: inputValue,
            confirmButtonColor: "crimson",
            inputValidator: (value) => {
              return new Promise((resolve) => {
                if (value.length === 0) {
                  resolve("일정의 이름을 입력하세요.");
                } else {
                  resolve();
                }
              });
            },
          },
          {
            icon: "info",
            title: "일정의 날짜를 입력하세요.",
            html: `<input style="width:100%;" id="datepicker" type="date" value="${inputValue}">`,
            focusConfirm: false,
            allowOutsideClick: false,
            confirmButtonColor: "crimson",
            preConfirm: () => {
              if (document.getElementById("datepicker").value) {
                return this.datetoint(
                  document.getElementById("datepicker").value
                );
              } else {
                return this.datetoint(inputValue);
              }
            },
          },
        ])
        .then(async (result) => {
          if (result.value) {
            this.actionScheduleName(result.value[0]);
            this.actionScheduleDate(result.value[1]);
            this.scheduleName = result.value[0];
            this.scheduleDate = result.value[1];

            let date = result.value[1];

            //스케줄 DB에 있나 확인하기
            const requestHeaders = {
              headers: {
                Authorization: `JWT ${this.$cookies.get("auth-token")}`,
              },
            };
            const data = {
              date: date,
            };
            this.$axios
              .post("/trip/date_chk", data, requestHeaders)
              .then((res) => {
                if (res.data) {
                  Swal.fire({
                    icon: "warning",
                    title: "이미 등록한 일정이 있습니다. 덮어쓰시겠습니까?",
                    allowOutsideClick: false,
                    showDenyButton: true,
                    denyButtonText: `Don't save`,
                    confirmButtonColor: "crimson",
                    denyButtonColor: "gray",
                  })
                    .then((result) => {
                      if (result.isDenied) {
                        this.$router.push({ name: "MyPageView" });
                      } else {
                        this.$axios
                          .post("/trip/delete/date_chk", data, requestHeaders)
                          .then(() => {
                            // empty block
                          });
                      }
                    })
                    .catch((err) => {
                      console.error(err);
                      this.$router.push({ name: "MyPageView" });
                    });
                } else {
                  Swal.fire({
                    icon: "success",
                    title: "일정 등록을 시작합니다",
                    confirmButtonColor: "crimson",
                  });
                }
              })
              .catch((err) => {
                console.log(err);
              });

            // if (this.getIsSik) {
            //   this.$router.push({ name: "SikdorangRecommendView" });
            // } else {
            //   this.$router.push({ name: "MapMain" });
            // }
            //   }
            // })
            // .catch((error) => {
            //   console.error(error);
            // });
          } else {
            this.$router.push("/");
          }
        });
    },
    // function about drag and drop
    handleClone(item) {
      let cloneMe = JSON.parse(JSON.stringify(item));
      this.$delete(cloneMe, "uid");
      return cloneMe;
    },
    deleteItem(index) {
      this.clonedItems.splice(index, 1);
    },

    //일정 관련 이름,날짜,내용 초기화
    resetScheduleStoreInfo() {
      this.actionScheduleName("");
      this.actionScheduleDate("");
      this.actionSchedule([]);
      this.actionScheduleIdx(0);
    },
    // function about trips
    getTripdata() {
      // getTripdata 유저 정보 받는 쪽으로 수정
      this.$axios
        .get(`/trip/list/${this.userId}`)
        .then((response) => {
          const data = response.data;
          for (let i = 0; i < data.length; i++) {
            this.saved.push({
              id: data[i].id,
              name: data[i].name,
              plan: data[i].plan,
            });
          }
        })
        .catch((error) => {
          console.error(error);
        });
    },
    createPlan() {
      if (this.clonedItems.length === 0) {
        Swal.fire({
          icon: "error",
          title: "일정을 등록하세요.",
          confirmButtonColor: "crimson",
        });
        return false;
      }
      let plan = "";
      const schedule = [];
      // console.log("일정을 추가했습니다.", this.clonedItems);
      if (this.getIsSik) {
        this.availableItems[0].idx = 0;
        schedule.push(this.availableItems[0]);
        plan = plan + schedule[0].id + 1234 + "-";
      }
      for (let i = 0; i < this.clonedItems.length; i++) {
        const item = this.clonedItems[i];
        if (this.getIsSik) {
          item["idx"] = i + 1;
        } else {
          item["idx"] = i;
        }
        // console.log(item);
        schedule.push(item);
        plan = plan + this.clonedItems[i].id + this.clonedItems[i].uid + "-";
      }
      // console.log("확인", plan, schedule);
      this.actionSchedule(schedule);
      this.actionScheduleIdx(0);
      this.actionFlip(true);
      this.actionMapEventClear("clear");
      this.actionClearBeforeCat();
      return plan;
    },
    datetostring(date) {
      var y = date.substr(0, 4);
      var m = parseInt(date.substr(6, 2));
      if (m < 10) {
        m = "0" + m;
      }
      var d = parseInt(date.substr(9, 2));
      if (d < 10) {
        d = "0" + d;
      }
      return y + "-" + m + "-" + d;
    },
    datetoint(date) {
      var y = date.substr(0, 4) * 10000;
      var m = parseInt(date.substr(5, 2)) * 100;
      var d = date.substr(8, 2) * 1;
      return y + m + d;
    },
    async checkIsScheduleDate(date) {
      const requestHeaders = {
        headers: {
          Authorization: `JWT ${this.$cookies.get("auth-token")}`,
        },
      };
      const data = {
        date: date,
      };
      this.$axios
        .post("/trip/date_chk", data, requestHeaders)
        .then((res) => {
          return res.data;
        })
        .catch((err) => {
          console.log(err);
        });
    },
    async createTrip() {
      let plan = this.createPlan();
      if (!plan) {
        return;
      }
      if (this.getIsSik) {
        this.$router.push({ name: "SikdorangRecommendView" });
      } else {
        this.$router.push({ name: "MapMain" });
      }
    },
    readTrip(item) {
      let trip = item.plan.split("-");
      this.clonedItems = [];
      for (let i = 0; i < trip.length; i++) {
        if (trip[i][0] == "R") {
          this.clonedItems.push({
            name: "식당",
            id: "R",
            uid: trip[i].slice(1),
          });
        } else if (trip[i][0] == "C") {
          this.clonedItems.push({
            name: "카페",
            id: "C",
            uid: trip[i].slice(1),
          });
        } else if (trip[i][0] == "S") {
          this.clonedItems.push({
            name: "관광지",
            id: "S",
            uid: trip[i].slice(1),
          });
        } else if (trip[i][0] == "A") {
          this.clonedItems.push({
            name: "숙박",
            id: "A",
            uid: trip[i].slice(1),
          });
        }
      }
    },
    updateTrip(item) {
      let plan = this.createPlan();
      if (!plan) {
        return;
      }
      const inputName = item.name;
      const inputDate = item.date;

      Swal.mixin({
        confirmButtonText: "Next &rarr;",
        showCancelButton: true,
        progressSteps: ["1", "2"],
      })
        .queue([
          {
            icon: "info",
            title: "일정의 이름을 입력하세요.",
            input: "text",
            inputValue: inputName,
            inputValidator: (value) => {
              return new Promise((resolve) => {
                if (value.length === 0) {
                  resolve("일정의 이름을 입력하세요.");
                } else {
                  resolve();
                }
              });
            },
          },
          {
            icon: "info",
            title: "일정의 날짜를 입력하세요.",
            html: `<input id="datepicker" type="date" value="inputValue">`,
            focusConfirm: false,
            preConfirm: () => {
              if (document.getElementById("datepicker").value) {
                return this.datetoint(
                  document.getElementById("datepicker").value
                );
              } else {
                return inputDate;
              }
            },
          },
        ])
        .then((result) => {
          if (result.value) {
            this.actionScheduleName(result.value[0]);
            this.actionScheduleDate(result.value[1]);
            this.$axios
              .put(`/trip/${item.id}/`, {
                user: this.userId,
                name: result.value,
                plan: plan.slice(0, -1),
              })
              .then((response) => {
                if (parseInt(response.status / 100) == 2) {
                  Swal.fire({
                    icon: "success",
                    title: "일정을 수정했습니다.",
                    confirmButtonColor: "crimson",
                  });
                }
              })
              .catch((error) => {
                console.error(error);
              });
          }
        });
    },
    deleteTrip(item) {
      Swal.fire({
        title: "일정을 삭제합니다.",
        text:
          "확인 버튼을 누르면 모든 데이터가 영구적으로 삭제되어 복구할 수 없게 됩니다.",
        icon: "warning",
        showCancelButton: true,
        confirmButtonColor: "crimson",
      }).then((result) => {
        if (result.value) {
          this.$axios
            .delete(`/trip/${item.id}/`)
            .then((response) => {
              if (parseInt(response.status / 100) == 2) {
                Swal.fire({
                  title: "일정이 삭제되었습니다.",
                  icon: "success",
                  showConfirmButton: true,
                  confirmButtonColor: "crimson",
                });
              }
            })
            .catch((error) => {
              console.error(error);
            });
        }
      });
    },
  },
};
</script>

<style>
.board {
  width: 100%;
  height: 50vh;
  overflow: auto;
  scrollbar-width: none;
  -ms-overflow-style: none;
  border: dashed 3px crimson;
}
board::-webkit-scrollbar {
  display: none;
}

.board > .availableItem {
  display: none;
}
.swal2-popup {
  font-family: "NIXGONM-Vb";
  font-size: 0.7rem !important;
}
.schedule-small {
  font-size: 10px !important;
}
.schedule-date {
  font-size: 14px !important;
}

.clickable-btn {
  width: 90%;
  background-color: white !important;
  border: 2px solid crimson !important;

}
.r-border {
  border: 2px solid tomato;
  width: 60px;
  height: 60px;
  border-radius: 50%;
  margin: 0px 10px;
}
.c-border {
  border: 2px solid sienna;
  width: 60px;
  height: 60px;
  border-radius: 50%;
  margin: 0px 10px;

}
.s-border {
  border: 2px solid steelblue;
  width: 60px;
  height: 60px;
  border-radius: 50%;
  margin: 0px 10px;
}
.a-border {
  border: 2px solid seagreen;
  width: 60px;
  height: 60px;
  border-radius: 50%;
  margin: 0px 10px;
}

</style>
