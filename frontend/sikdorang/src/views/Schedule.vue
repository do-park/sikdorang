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

    <v-btn @click="createPlan(clonedItems)">완료</v-btn>
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
  methods: {
    handleClone(item) {
      // Create a fresh copy of item
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

    createPlan(items) {
      let R = 0;
      let C = 0;
      let S = 0;
      let A = 0;
      let plan = "";
      for (let i = 0; i < items.length; i++) {
        if (items[i].name === "R") {
          plan = plan + "R" + R + "-";
          R += 1;
        } else if (items[i].id === "C") {
          plan = plan + "C" + C + "-";
          C += 1;
        } else if (items[i].id === "S") {
          plan = plan + "S" + S + "-";
          S += 1;
        } else {
          plan = plan + "A" + A + "-";
          A += 1;
        }
      }
      console.log(plan.slice(0, -1));
    },
  },
};
</script>

<style>
</style>
