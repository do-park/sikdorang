<template>
  <div class="map-top">
    <swiper class="swiper" :options="swiperOption">
      <swiper-slide v-for="(tag, idx) in tags" :key="idx" class="mr-1 pr-3">
        <button
          @click="onClick(tag)"
          style="background:crimson;"
          class="text-white rounded"
        >
          #{{ tag }}
        </button>
      </swiper-slide>
    </swiper>
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
.map-top {
  position: absolute;
  z-index: 10;
  width: 500px;
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
