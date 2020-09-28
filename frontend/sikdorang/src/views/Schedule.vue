<template>
  <div>
    <h1>오늘의 일정</h1>
    <p>일정을 삭제하려면 클릭하세요.</p>
    <draggable
      v-model="clonedItems"
      :options="clonedItemOptions"
      style="border: 1px solid blue"
    >
      <v-btn
        v-for="(item, index) in clonedItems"
        :key="index"
        @click="deleteItem(index)"
        class="clickable"
        >{{ item.name }}</v-btn
      >
    </draggable>

    <div style="height: 50px"></div>

    <draggable
      v-model="availableItems"
      :options="availableItemOptions"
      :clone="handleClone"
    >
      <v-btn v-for="(item, index) in availableItems" :key="index">{{
        item.name
      }}</v-btn>
    </draggable>

    <div style="height: 50px"></div>

    <v-btn @click="createTrip()">CREATE</v-btn>
    <br />
    <span v-for="(item, index) in saved" :key="index">
      <v-btn @click="readTrip(item)">READ {{ index }}</v-btn>
      <v-btn @click="updateTrip(item)">UPDATE {{ index }}</v-btn>
      <v-btn @click="deleteTrip(item)">DELETE {{ index }}</v-btn>
      <br />
    </span>
  </div>
</template>

<script>
import draggable from "vuedraggable";
import Swal from "sweetalert2";
import { mapActions } from "vuex";

export default {
  name: "Schedule",
  order: 2,
  components: {
    draggable,
  },
  data() {
    return {
      userId: null,
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
  created() {
    // todo: userId에 현재 로그인한 유저의 id 넣어주기
    // this.userId = 1;
    // this.getTripdata();
  },
  methods: {
    ...mapActions("schedule", [
      "actionSchedule",
      "actionScheduleIdx",
      "actionScheduleName",
      "actionScheduleDate",
    ]),
    ...mapActions("mapEvent", ["actionFlip", "actionMapEventClear"]),
    // function about drag and drop
    handleClone(item) {
      let cloneMe = JSON.parse(JSON.stringify(item));
      this.$delete(cloneMe, "uid");
      return cloneMe;
    },
    deleteItem(index) {
      this.clonedItems.splice(index, 1);
    },
    uuid(e) {
      if (e.uid) return e.uid;
      const key = Math.random().toString(10).slice(2);
      this.$set(e, "uid", key);
      return e.uid;
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

      for (let i = 0; i < this.clonedItems.length; i++) {
        const item = this.clonedItems[i];
        item["idx"] = i;
        schedule.push(item);
        plan = plan + this.clonedItems[i].id + this.clonedItems[i].uid + "-";
      }
      this.actionSchedule(schedule);
      this.actionScheduleIdx(0);
      this.actionFlip(true);
      this.actionMapEventClear("clear");
      return plan;
    },
    datetostring(date) {
      var y = date.substr(0, 4);
      var m = parseInt(date.substr(5, 2));
      if (m < 10) {
        m = "0" + m;
      }
      var d = date.substr(9, 2);
      return y + "-" + m + "-" + d;
    },
    createTrip() {
      let plan = this.createPlan();
      if (!plan) {
        return;
      }
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
            html: `<input id="datepicker" type="date" value="inputValue">`,
            focusConfirm: false,
            preConfirm: () => {
              if (document.getElementById("datepicker").value) {
                return document.getElementById("datepicker").value;
              } else {
                return inputValue;
              }
            },
          },
        ])
        .then((result) => {
          if (result.value) {
            this.actionScheduleName(result.value[0]);
            this.actionScheduleDate(result.value[1]);
            // this.$axios
            //   .post(`/trip/`, {
            //     user: this.userId,
            //     name: result.value,
            //     plan: plan.slice(0, -1),
            //   })
            // .then((response) => {
            //   if (parseInt(response.status / 100) == 2) {
            Swal.fire({
              icon: "success",
              title: "일정을 등록했습니다.",
            });
            this.$router.push({ name: "MapMain" });
            //   }
            // })
            // .catch((error) => {
            //   console.error(error);
            // });
          }
        });
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
                return document.getElementById("datepicker").value;
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
</style>
