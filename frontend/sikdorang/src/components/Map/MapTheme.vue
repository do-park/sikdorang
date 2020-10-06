<template>
  <div>
    <div class="map-top d-none">
      <swiper class="swiper" :options="swiperOption">
        <swiper-slide v-for="(tag, idx) in tags" :key="idx">
          <div
            @click="onClick(tag)"
            class="txt"
          >
            #{{ tag }}
          </div>
        </swiper-slide>
      </swiper>
    </div>
    <div class="map-top">
      <swiper class="swiper" :options="swiperOption">
        <swiper-slide v-for="(tag, idx) in tags" :key="idx">
          <div
            @click="onClick(tag)"
            class="txt"
          >
            #{{ tag }}
          </div>
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
        // slidesPerView: 4,
        // spaceBetween: 10,
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
  display: inline-block;
  background-color: crimson;
  color: white;
  font-size: 16px;
  width: 100%;
  padding: 0.3rem 0.5rem;
  border-radius: 30%;
}
.map-top {
  position: absolute;
  z-index: 10;
  width: 100%;
  max-width: 600px;
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
  width: auto !important;
  padding: 0.5rem;
}
.swiper-container {
  height: 60px;
}
</style>
