<template>
  <section class="slider">
    <ul class="slider__list" ref="list">
      <li
        v-for="theme in themes"
        :key="theme.id"
        class="slider__item"
        v-tap="(e) => onTap(e, theme)"
      >
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
      </li>
    </ul>
  </section>
</template>

<script
  src="https://cdnjs.cloudflare.com/ajax/libs/hammer.js/2.0.8/hammer.min.js"
  integrity="sha512-UXumZrZNiOwnTcZSHLOfcTs0aos2MzBWHXOHOuB0J/R44QB0dwY5JgfbvljXcklVf65Gc4El6RjZ+lnwd2az2g=="
  crossorigin="anonymous"
></script>
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
      currentOffset: 0,
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
  computed: {
    overflowRatio() {
      return this.$refs.list.scrollWidth / this.$refs.list.offsetWidth;
    },
    itemWidth() {
      return this.$refs.list.scrollWidth / this.themes.length;
    },
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
    onPan(e) {
      const dragOffset =
        (((100 / this.itemWidth) * e.deltaX) / this.count) * this.overflowRatio;

      const transform = this.currentOffset + dragOffset;

      this.$refs.list.style.setProperty("--x", transform);

      if (e.isFinal) {
        this.currentOffset = transform;
        const maxScroll = 100 - this.overflowRatio * 100;
        let finalOffset = this.currentOffset;

        // scrolled to last item
        if (this.currentOffset <= maxScroll) {
          finalOffset = maxScroll;
        } else if (this.currentOffset >= 0) {
          // scroll to first item
          finalOffset = 0;
        } else {
          // animate to next item according to pan direction
          const index =
            (this.currentOffset / this.overflowRatio / 100) * this.count;
          const nextIndex =
            e.deltaX <= 0 ? Math.floor(index) : Math.ceil(index);
          finalOffset = ((100 * this.overflowRatio) / this.count) * nextIndex;
        }

        // bounce back animation
      }
    },
  },
};
</script>

<style scoped lang="scss">
.slider {
  width: 100%;
  height: 120px;
  overflow: visible;
  position: relative;
  white-space: nowrap;

  &__list {
    display: flex;
    width: 100%;
    height: 100%;

    font-size: 2rem;
    backface-visibility: hidden;
    transform: translateX(calc(var(--x, 0) * 1%));
  }

  &__item {
    position: relative;
    flex: 0 0 140px;

    display: flex;
    justify-content: center;
    align-items: center;
    height: 100%;
    margin-right: 12px;
    padding: 6px;
    box-sizing: border-box;

    border-radius: 8px;
    text-align: center;
    transition: opacity 0.15s ease;
    color: #fff;

    &:focus {
      opacity: 0.8;
    }
  }
}
</style>

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
