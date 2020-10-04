<template>
  <swiper class="swiper" :options="swiperOption">
    <swiper-slide v-for="theme in themes" :key="theme.id" class="m-0">
      <span v-if="userAchieve[theme.db_id] === 1" class="effect">
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

      <div>{{ theme.theme_name }}</div>
    </swiper-slide>
    <div class="swiper-pagination" slot="pagination"></div>
  </swiper>
</template>

<script>
import { Swiper, SwiperSlide } from "vue-awesome-swiper";
import "swiper/swiper-bundle.css";
import { mapGetters, mapActions } from "vuex";
const themes = "themes";

export default {
  name: "ThemePage",
  components: {
    Swiper,
    SwiperSlide,
  },
  data() {
    return {
      isLogin: this.$store.state.isLogin,
      themes: [],
      userAchieve: [],
      swiperOption: {
        slidesPerView: 4,
        spaceBetween: 10,
        pagination: {
          el: ".swiper-pagination",
          clickable: true,
        },
      },
    };
  },
  computed: {
    ...mapGetters(themes, ["getThemes", "getThemesClear"]),
  },
  created() {},
  mounted() {
    this.themes = this.getThemes;
    this.getAchievedata();
  },
  methods: {
    ...mapActions(themes, ["actionThemesClear", "actionStoreClear"]),
    goDetail(theme) {
      this.$cookies.set("theme_id", theme.id);
      this.$cookies.set("theme_name", theme.theme_name);
      this.$router.push("/themedetail");
    },
    getAchievedata() {
      if (this.isLogin) {
        const requestHeaders = {
          headers: {
            Authorization: `JWT ${this.$cookies.get("auth-token")}`,
          },
        };
        this.$axios
          .get(`achievement/theme_clear`, requestHeaders)
          .then((res) => {
            this.actionThemesClear(res.data[0]);
            this.userAchieve = res.data[0];
            this.actionStoreClear(res.data[1]);
          })
          .catch((err) => {
            console.log(err);
          });
      } else {
        this.userAchieve = [0, 0, 0, 0, 0, 0, 0, 0, 0];
      }
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
.swiper-slide {
  display: flex;
  justify-content: center;
  flex-direction: column;
}
.swiper-container {
  height: 150px;
  width: 100%;
}
</style>
