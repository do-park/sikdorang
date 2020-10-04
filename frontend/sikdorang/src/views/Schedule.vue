<template>
  <div>
    <h3 class="mt-1 ml-1">{{ scheduleName }}</h3>
    <!-- <div class="d-flex flex-row justify-content-between"> -->
    <!-- </div> -->
    <p class="text-right">
      날짜: {{ scheduleDate.toString().substr(0, 4) }}-{{
        scheduleDate.toString().substr(4, 2)
      }}-{{ scheduleDate.toString().substr(6, 2) }}
    </p>
    <p class="text-right" v-if="getIsSik">
      {{ getForUser.store_name }}에서 일정을 시작합니다.
    </p>

    <draggable v-model="clonedItems" :options="clonedItemOptions" class="board">
      <v-btn
        v-for="(item, index) in clonedItems"
        :key="index"
        @click="deleteItem(index)"
        class="clickable my-2 mx-1 d-block"
        style="width: 98%"
      >
        <i v-if="item.id == 'R'" class="fas fa-utensils" style="color: red">
          {{ item.name }}</i
        >
        <i v-if="item.id == 'C'" class="fas fa-coffee" style="color: brown">
          {{ item.name }}</i
        >
        <i
          v-if="item.id == 'S'"
          class="fas fa-place-of-worship"
          style="color: blue"
        >
          {{ item.name }}</i
        >
        <i v-if="item.id == 'A'" class="fas fa-bed" style="color: green">
          {{ item.name }}</i
        >
      </v-btn>
    </draggable>

    <p class="text-right mt-0 small">
      *아이콘을 상자에 끌어 넣어 일정을 구성해보세요. 클릭하면 삭제됩니다.
    </p>
    <div style="height: 5vh"></div>
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
        <i v-if="item.id == 'R'" class="fas fa-utensils" style="color: red"></i>

        <i v-if="item.id == 'C'" class="fas fa-coffee" style="color: brown"></i>

        <i
          v-if="item.id == 'S'"
          class="fas fa-place-of-worship"
          style="color: blue"
        ></i>

        <i v-if="item.id == 'A'" class="fas fa-bed" style="color: green"></i>
      </button>
    </draggable>

    <div style="height: 5vh"></div>

    <div class="d-flex justify-content-center">
      <v-btn @click="createTrip()">CREATE</v-btn>
    </div>
    <br />
    <!-- <span v-for="(item, index) in saved" :key="index">
      <v-btn @click="readTrip(item)">READ {{ index }}</v-btn>
      <v-btn @click="updateTrip(item)">UPDATE {{ index }}</v-btn>
      <v-btn @click="deleteTrip(item)">DELETE {{ index }}</v-btn>
      <br />
    </span> -->
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
    console.log("게터 확인", this.getIsSik, this.getForUser);
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
      console.log(inputValue);
      inputValue = this.datetostring(inputValue);
      console.log(inputValue);

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
              .post("trip/date_chk", data, requestHeaders)
              .then((res) => {
                if (res.data) {
                  Swal.fire({
                    icon: "warning",
                    title: "이미 등록한 일정이 있습니다. 덮어쓰시겠습니까?",
                    allowOutsideClick: false,
                    showDenyButton: true,
                    denyButtonText: `Don't save`,
                  })
                    .then((result) => {
                      console.log(result);
                      if (result.isDenied) {
                        this.$router.push({ name: "MyPageView" });
                      } else {
                        this.$axios
                          .post("trip/delete/date_chk", data, requestHeaders)
                          .then((res) => {
                            console.log(res, "삭제 완료");
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
                  });
                  console.log(
                    "이름 날짜 확인",
                    result.value[0],
                    result.value[1]
                  );
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
      console.log("스케줄 관련 다 초기화 합니다.");
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
      console.log(data);
      this.$axios
        .post("trip/date_chk", data, requestHeaders)
        .then((res) => {
          console.log("값 왔냐?", res);
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
  background: lightsalmon;
}
board::-webkit-scrollbar {
  display: none;
}
.availableItem {
  width: 50px;
  height: 50px;
  margin: 0px 10px;
}
.swal2-popup {
  font-family: "NIXGONM-Vb";
  font-size: 0.7rem !important;
}
</style>
