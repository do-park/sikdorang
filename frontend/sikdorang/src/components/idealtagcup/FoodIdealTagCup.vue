<template>
  <div>
    <h3 class="text-center">{{ gameCount}} | {{ roundCount }}</h3>
    <div v-if="!isDone">
      <img
        class="img"
        :src="imgs[tags[leftIndex]]"
        alt="left Image"
        @click="onClick('left')"
      />
    </div>
    <div class="vs-wrap" v-if="!isDone">
      <img class="vs" src="@/assets/vs.png" />
    </div>
    <div v-if="!isDone">
      <img
        class="img"
        :src="imgs[tags[rightIndex]]"
        alt="right Image"
        @click="onClick('right')"
      />
    </div>
    <div v-if="isDone" @click="done">
      <img :src="imgs[tags[0]]" />
    </div>
  </div>
</template>

<script>
import Swal from "sweetalert2";

export default {
  name: "FoodIdealTagCup",
  data() {
    return {
      imgs: [
        require("@/assets/food_cup/hansik.jpg"),
        require("@/assets/food_cup/bunsik.jpg"),
        require("@/assets/food_cup/pizza.jpg"),
        require("@/assets/food_cup/chicken.jpg"),
        require("@/assets/food_cup/don_Hoe_ilsik.jpg"),
        require("@/assets/food_cup/cafe_dessert_bakery.jpg"),
        require("@/assets/food_cup/asian.jpg"),
        require("@/assets/food_cup/western.jpg"),
        require("@/assets/food_cup/chinese.jpg"),
        require("@/assets/food_cup/dosirak.jpg"),
        require("@/assets/food_cup/fastfood.jpg"),
        require("@/assets/food_cup/alcohol.jpg"),
        require("@/assets/food_cup/jokbal.jpg"),
        require("@/assets/food_cup/zzim_tang.jpg"),
      ],
      tags: [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13],
      leftIndex: 0,
      rightIndex: 1,
      round: 1,
      clickCount: -1,
      userChoice: [],
      isDone: false,
      isSaved: false,
    };
  },
  computed: {
    roundCount() {
      if (this.tags.length === 2) {
        return '결승'
      } else if (this.tags.length === 1) {
        return '우승'
      } else {
        return `${this.tags.length} 강`
      }
    },
    gameCount() {
      if (this.clickCount === -1) {
        return `1 / ${Math.round(this.tags.length / 2)}`
      } else if (this.clickCount === 1) {
        return `2 / ${Math.round(this.tags.length / 2)}`
      } else {
        return `${Math.round(this.clickCount / 2)+1} / ${Math.round(this.tags.length / 2)}`
      }
    }
  },
  mounted() {
    Swal.fire({
      title: '<strong>음식 종류 이상형 월드컵</strong>',
      icon: 'info',
      html:
        '<p>어떤 음식을 가장 좋아하시나요?</p>' +
        '<strong>이상형 월드컵으로 알아보세요!</strong>'
    })
  },
  methods: {
    onClick(direction) {
      console.log(this.clickCount)
      this.clickCount += 2;
      // 선택한 이미지를 userChoice에 추가합니다.
      if (direction === "left") {
        this.userChoice.push(this.tags[this.leftIndex]);
      } else {
        this.userChoice.push(this.tags[this.rightIndex]);
      }
      // clickCount가 배열보다 같거나 크다면 다음 라운드로 진행합니다.
      if (this.clickCount >= this.tags.length - 1) {
        this.nextRound();
      } else {
        this.leftIndex = this.leftIndex + 2;
        this.rightIndex = this.rightIndex + 2;
        // rightIndex가 배열의 마지막 인덱스보다 큰 값이라면 부전승 시킵니다.
        if (this.rightIndex > this.tags.length - 1) {
          this.userChoice.push(this.tags[this.leftIndex]);
          this.nextRound();
        }
      }
      if (this.tags.length == 4 && !this.isSaved) {
        this.tagsSave();
        this.isSaved = true;
      }
    },
    nextRound() {
      // tags를 userChocie로 갱신하고 나머지 정보를 초기화합니다.
      this.tags = this.userChoice;
      this.userChoice = [];
      this.round += 1;
      this.clickCount = -1;
      // tags의 길이가 1이라면 종료된 것이므로 게임을 종료합니다.
      if (this.tags.length === 1) {
        this.isDone = true;
      }
      this.leftIndex = 0;
      this.rightIndex = 1;
    },
    // 4강(3강이 되는 경우는 3강)이 되면 정보를 저장합니다.
    tagsSave() {
      const requestHeaders = {
        headers: {
          Authorization: `JWT ${this.$cookies.get("auth-token")}`,
        },
      };
      // console.log(this.tags);
      this.$axios
        .post("trip/idealcategory", { tags: this.tags }, requestHeaders)
        .then(() => {
          //empty
        })
        .catch((err) => console.error(err));
    },
    done() {
      Swal.fire({
        title: '<strong>음식점 장점 이상형 월드컵</strong>',
        icon: 'info',
        html:
          '<p>어떤 음식점을 가장 좋아하시나요?</p>' +
          '<strong>이상형 월드컵으로 알아보세요!</strong>'
      })
      this.$emit("done");
    },
  },
};
</script>

<style scoped>
.img {
  width: 400px;
  cursor: pointer;
}
.vs-wrap {
  position: relative;
  widows: 400px;
}
.vs {
  width: 100px;
  left: 50%;
  transform: translateX(-50%);
  bottom: -40px;
  position: absolute;
}
</style>