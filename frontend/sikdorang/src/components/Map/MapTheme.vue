<template>
  <div>
    <div class="map-top d-none d-md-block">
      <swiper class="swiper" :options="swiperOption">
        <swiper-slide v-for="(tag, idx) in tags" :key="idx">
          <button
            @click="onClick(tag)"
            style="background: crimson"
            class="text-white rounded txt2"
          >
            #{{ tag }}
          </button>
        </swiper-slide>
      </swiper>
    </div>
    <div class="map-top d-block d-md-none">
      <swiper class="swiper" :options="swiperOption">
        <swiper-slide v-for="(tag, idx) in tags" :key="idx">
          <button
            @click="onClick(tag)"
            style="background: crimson"
            class="text-white rounded txt"
          >
            #{{ tag }}
          </button>
        </swiper-slide>
      </swiper>
    </div>
  </div>
</template>

<script>
import { Swiper, SwiperSlide } from "vue-awesome-swiper";
import "swiper/swiper-bundle.css";
import { mapGetters, mapActions } from "vuex";

export default {
  name: "MapTheme",
  components: {
    Swiper,
    SwiperSlide,
  },
  data() {
    return {
      destination: "",
      tags: [],
      swiperOption: {
        slidesPerView: 5,
        spaceBetween: 20,
        pagination: {
          el: ".swiper-pagination",
          clickable: true,
        },
      },
    };
  },
  computed: {
    ...mapGetters("mapEvent", ["getTags"]),
  },
  watch: {
    getTags() {
      this.tags = this.getTags;
    },
  },
  methods: {
    ...mapActions("mapEvent", ["actionSelectTag"]),
    onClick(tag) {
      this.actionSelectTag(tag);
    },
  },
};
</script>

<style scoped>
.txt {
  height: 50px;
  width: 20vw;
  margin-right: 10vw;
}
.txt2 {
  width: 100px;
}
.map-top {
  position: absolute;
  z-index: 10;
  width: 100%;
}

#search-box {
  width: 342px;
  height: 30px;
  float: left;
}

#search-btn {
  width: 50px;
  height: 36px;
  float: right;
}

.tag-tap {
  width: 400px;
  margin: auto;
}

.tag-tap > button {
  margin: 10px;
  background-color: yellow;
}
.swiper-slide {
  display: flex;
  justify-content: center;
  flex-direction: column;
}
.swiper-container {
  height: 100px;
  width: 100%;
}
</style>
