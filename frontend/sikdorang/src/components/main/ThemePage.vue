<template>
<div>
  <h5 class="theme-title"><i class="fas fa-flag-checkered"></i> 맛집 도장깨기 </h5>
  <hr>
<div class="container">
  <div class="row">
    <div 
    v-for="theme in themes" 
    :key="theme.id" 
    class="col-2 m-0 p-1" 
    >
      <div 
      v-if="userAchieve[theme.db_id] === 1" 
      class="effect"
      > 
        <div @click="goDetail(theme)">
          <img
            class="img-circle"
            :src="require(`../../../public/icons/${theme.id}.png`)"
          />
          <div class="theme-name mx-auto">{{ theme.theme_name }}</div>
        </div>
      </div>
      <div v-else >
        <div @click="goDetail(theme)">
          <img
              class="img-circle"
              :src="require(`../../../public/icons/${theme.id}.png`)"
            />
            <div class="theme-name mx-auto">{{ theme.theme_name }}</div>
        </div>
      </div>
    </div>
  </div>

</div>
</div>
</template>

<script>
import { mapGetters, mapActions } from "vuex";
const themes = "themes";

export default {
  name: "ThemePage",
  data() {
    return {
      isLogin: this.$store.state.isLogin,
      themes: [],
      userAchieve: [],
    };
  },
  computed: {
    ...mapGetters(themes, ["getThemes", "getThemesClear"]),
  },
  created() {},
  mounted() {
    this.themes = this.getThemes;
    if (this.themes.length < 12) {
      this.themes.push({
        id : 12,
        db_id : 12,
        theme_name : "준비중"
      })

    }
    this.getAchievedata();
  },
  methods: {
    ...mapActions(themes, ["actionThemesClear", "actionStoreClear"]),
    getCardBgImage(image_url) {
      console.log("여기 주소",image_url)
      return 'background-image: url("' + image_url + '")';
    },
    
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
          .get(`/achievement/theme_clear`, requestHeaders)
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
  width: 100%;
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
  height: auto;
  background: crimson;
  border: 3px solid crimson;
  content: "Clear";
  text-align: center;
  color: #fff;
  font-family: "Arial";
  font-weight: bold;
  font-size: 3vmin;
  transform: rotate(-25deg);
  left: 5px;
  top: 10px;
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
.isFour {
  border: 5px solid gray;
  min-height : 70px;
  min-width : 30px;
};
.isTopBottom {
  border-top: 5px solid gray;
  border-bottom: 5px solid gray;
  min-height : 70px;
  min-width : 30px;
};
.isSide{
  border-left: 5px solid gray;
  border-right: 5px solid gray;
  min-height : 70px;
  min-width : 30px;
}
.theme-name{
  font-size: 3vmin;
  text-align : center;
  width : 100%;
  font-weight: bold;
}
.theme-title{
  font-size: 16px;
  text-align : left;
  font-weight: bold;
}

</style>
