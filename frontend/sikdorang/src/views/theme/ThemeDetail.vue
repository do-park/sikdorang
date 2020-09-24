<template>
  <div>
    <h1>명예의 전당 [ {{theme_name}} ]편</h1>
    <div class="container">
      <div class="row text-center">
        <div
          @click="goDetail(restuarant, index)"
          v-for="(restuarant, index) in restaurants"
          :key="restuarant.id"
          class="box col-sm-4 m-0"
        >
          <span v-if="userVisited[index] === 1" class="effect">
            <div class="img-card" :style="getCardBgImage(`${IMG_URL}${restuarant.image}`)">
              <p class="store_name">{{restuarant.store_name}}</p>
            </div>
          </span>
          <span v-else>
            <div class="img-card" :style="getCardBgImage(`${IMG_URL}${restuarant.image}`)">
              <p class="store_name">{{restuarant.store_name}}</p>
            </div>
          </span>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import Swal from "sweetalert2";
export default {
  name: "ThemeDetail",
  data() {
    return {
      theme_name: this.$cookies.get("theme_name"),
      theme_id: this.$cookies.get("theme_id"),
      restaurants: [
        { id: 111, store_name: "빵집1" },
        { id: 222, store_name: "빵집2" },
        { id: 333, store_name: "빵집3" },
      ],
      IMG_URL: "http://j3d202.p.ssafy.io:8080",
      userId: null,
      userVisited: [],
    };
  },
  created() {
    // todo: userId에 현재 로그인한 유저의 id 넣어주기
    this.userId = 1;
    this.getRestarants();
    this.getMyVisited(1);
  },
  methods: {
    getCardBgImage(image_url) {
      return 'background-image: url("' + image_url + '")';
    },
    getRestarants() {
      console.log(this.theme_id);
      this.$axios  
        .get(`/achievement/${this.theme_id}`)
        .then((res) => {
          var restaurants = res.data;
          this.restaurants = restaurants;
        })
        .catch((err) => {
          console.log(err);
        });
    },
    getMyVisited(userId) {
      //나중에 axios로 받아오면 이거 지워주세요.
      this.userVisited = [1, 1, 1, 0, 0, 0, 0, 0, 0];

      // todo: axios로 Back에서 user의 achievedata 받아오기
      console.log(userId);

      // this.$axios.get(`/achievement/${this.theme_id}/${userId}`)
      // .then(res => {
      //     var userVisited = res.data
      //     this.userVisited = userVisited
      // })
      // .catch(err => {
      //     console.log(err)
      // })
    },
    goDetail(rest, index) {
      //   swal(rest.store_name, rest.description);
      Swal.fire({
        title: rest.store_name,
        text: rest.description,
        showCancelButton: true,
        confirmButtonColor: "#3085d6",
        cancelButtonColor: "#d33",
        confirmButtonText: "방문하기",
        cancelButtonText: "OK",
      }).then((result) => {
        if (result.isConfirmed) {
          this.userVisited[index] = 1;
          Swal.fire("Yummy!", "테스트를 위한 방문 완료!", "success");
          console.log(this.userVisited);
          // todo: axios 처리도 해야할 것 같은데 Swal 안에서 할 수 있는지 모르겠군요
          // axios로 지금 이 식당에 방문했음으로 변경
          // 테마가 완료되었다면, axios로 테마 완성
        }
      });
    },
  },
};
</script>

<style scoped>
.box {
  height: 100px;
  width: 100px;
  background: blanchedalmond;
}
.img-card {
  height: 100px;
  width: 100px;
  background-size: cover;
}
.store_name {
  text-align: right;
  text-shadow: -1px 0 blanchedalmond, 0 1px blanchedalmond, 1px 0 blanchedalmond,
    0 -1px blanchedalmond;
  font-size: 14px;
  /* background-color: rgba(240, 240, 240, 0.3); */
}
.effect {
  position: relative;
  display: block;
  overflow: hidden;
  padding: 1px;
}
.effect:after {
  content: "";
  position: absolute;
  z-index: 1;
  width: 70px;
  height: auto;
  background: red;
  border: 3px solid red;
  content: "Clear";
  text-align: center;
  color: #fff;
  font-family: "Arial";
  font-weight: bold;
  /* padding: 5px 10px; */
  transform: rotate(-25deg);
  left: 3px;
  top: 20px;
  /* box-shadow: 0 1px 3px rgba(0, 0, 0, 0.3); */
}
</style>
