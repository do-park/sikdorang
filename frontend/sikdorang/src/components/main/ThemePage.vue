<template>
  <div class="row text-center m-1">
    <div v-for="(theme, index) in themes" :key="theme.id" class="m-1">
      <span v-if="userAchieve[index] == 'True'" class="effect">
        <img
          @click="goDetail(theme)"
          class="img-circle"
          :src="require(`../../../public/icons/${theme.id}.png`)"
        />
      </span>
      <span v-else>
        <img
          @click="goDetail(theme)"
          class="img-circle"
          :src="require(`../../../public/icons/${theme.id}.png`)"
        />
      </span>

      <div>{{theme.theme_name}}</div>
    </div>
  </div>
</template>

<script>
import { mapGetters } from "vuex";
const themes = "themes";

export default {
  name: "ThemePage",
  data() {
    return {
      themes: [],
      userId: null,
      userAchieve: [],
    };
  },
  computed: {
    ...mapGetters(themes, ["getThemes"]),
  },
  created() {
    // todo: userId에 현재 로그인한 유저의 id 넣어주기
    this.userId = 1;
    this.getAchievedata(this.userId);
  },
  mounted() {
    this.themes = this.getThemes;
    this.getAchievedata(this.userId);
    // console.log(this.themes)
  },
  methods: {
    goDetail(theme) {
      this.$cookies.set("theme_id", theme.id);
      this.$cookies.set("theme_name", theme.theme_name);
      this.$router.push("/themedetail");
    },
    getAchievedata(userId) {
      // todo: axios로 Back에서 user의 achievedata 받아오기
      console.log(userId);
      const data =
        "False,True,True,False,False,True,False,True,True,False,False";
      this.userAchieve = data.split(",");
    },
  },
};
</script>

<style scoped>
.box {
  background-color: blanchedalmond;
}
.img-circle {
  display: inline-block;
  width: 80px;
  height: 80px;
  border-radius: 40%;
  border: 3px solid black;
  background-color: rgba(0, 0, 0, 0.445);
  background-repeat: no-repeat;
  background-position: center center;
  background-size: cover;
}
.img-circle:hover {
  cursor: pointer;
}
.effect {
  position: relative;
  display: inline-block;
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
}
</style>