<template>
  <div>
    <h1>오늘의 일정</h1>
    <p>일정을 삭제하려면 클릭하세요.</p>
    <draggable v-model="clonedItems" :options="clonedItemOptions" style="border: 1px solid blue;">
      <v-btn
        v-for="(item, index) in clonedItems"
        :key="uuid(item)"
        @click="deleteItem(index)"
        class="clickable"
      >{{item.name}}</v-btn>
    </draggable>

    <div style="height:50px;"></div>

    <draggable v-model="availableItems" :options="availableItemOptions" :clone="handleClone">
      <v-btn v-for="item in availableItems" :key="uuid(item)">{{item.name}}</v-btn>
    </draggable>

    <div style="height:50px;"></div>

    <v-btn @click="createtrip(clonedItems)">CREATE</v-btn>
    <span v-for="(item, i) in saved" :key="item">
      <v-btn @click="readtrip(item, i)">READ {{i}}</v-btn>
      <v-btn @click="updatetrip(item, i)">UPDATE {{i}}</v-btn>
      <v-btn @click="deletetrip(item, i)">DELETE {{i}}</v-btn>
    </span>
  </div>
</template>

<script>
import draggable from "vuedraggable";

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
        },
        {
          name: "카페",
          id: "C",
        },
        {
          name: "관광지",
          id: "S",
        },
        {
          name: "숙박",
          id: "A",
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
  // todo: 현재 로그인한 유저의 정보를 받아와야 함, 일단 1 넣어주는걸로 test
  created() {
    this.userId = 1;
  },

  methods: {
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
    createtrip(items) {
      let R = 0;
      let C = 0;
      let S = 0;
      let A = 0;
      let trip = "";
      for (let i = 0; i < items.length; i++) {
        if (items[i].id === "R") {
          trip = trip + "R" + R + "-";
          R += 1;
        } else if (items[i].id === "C") {
          trip = trip + "C" + C + "-";
          C += 1;
        } else if (items[i].id === "S") {
          trip = trip + "S" + S + "-";
          S += 1;
        } else {
          trip = trip + "A" + A + "-";
          A += 1;
        }
      }
      // for test: console로 찍는 대신 백엔드로 넘길 수 있게 수정
      this.saved.push(trip.slice(0, -1));
      this.clonedItems = [];
      console.log(this.saved);
    },
    readtrip(item) {
      // for test: this.saved에서 꺼내오는 대신 백엔드에서 받아올 수 있게 수정
      let trip = item.split("-");
      this.clonedItems = [];
      console.log(trip);
      for (let i = 0; i < trip.length; i++) {
        if (trip[i][0] == "R") {
          this.clonedItems.push({
            name: "식당",
            id: "R",
          });
        } else if (trip[i][0] == "C") {
          this.clonedItems.push({
            name: "카페",
            id: "C",
          });
        } else if (trip[i][0] == "S") {
          this.clonedItems.push({
            name: "관광지",
            id: "S",
          });
        } else if (trip[i][0] == "A") {
          this.clonedItems.push({
            name: "숙박",
            id: "A",
          });
        }
      }
    },
    updatetrip(item, i) {
      // for test: this.saved에서 수정하는 대신 DB에서 수정해야 함
      // 사실상 지금 이 코드는 쓸모가 없다...ㅋㅋ
      console.log(item);
      console.log(i);
    },
    deletetrip(item, i) {
      // for test: this.saved에서 삭제하는 대신 DB에서 삭제해야 함
      // 사실상 지금 이 코드는 쓸모가 없다...ㅋㅋ
      console.log(item);
      console.log(i);
      if (i > -1) this.saved.splice(i, 1);
    },
  },
};
</script>

<style>
</style>
