<template>
  <div class="d-flex">
      <div 
      v-for="theme in themes" 
      :key="theme.id">
          <img
          v-if="getThemesClear[theme.id-1]"
          @click="goToThemeDetail(theme)"
          class="img-circle-sm"
          :src="require(`../../../public/icons/${theme.id}.png`)"
        />
      </div>
  </div>
</template>

<script>
import { mapGetters } from "vuex"
const themes = "themes"

export default {
    name : 'AchievementBadge',
    computed : {
        ...mapGetters(themes, [
            'getThemes',
            'getThemesClear',
        ])
    },
    data() {
        return {
            themes : [],
            themesClear : [],
        }
    },
    created() {
        this.themes = this.getThemes;
        this.themesClear = this.getThemesClear;
    },
    methods : {
        goToThemeDetail(theme) {
            console.log(theme.theme_name)
            this.$cookies.set('theme_name',theme.theme_name),
            this.$cookies.set('theme_id',theme.id),
            this.$router.push('/themedetail')
        },
    },
}
</script>

<style>
.img-circle-sm {
  display: inline-block;
  width: 40px;
  height: 40px;
  border-radius: 40%;
  border: 3px solid black;
  background-color: rgba(0, 0, 0, 0.3);
  background-repeat: no-repeat;
  background-position: center center;
  background-size: cover;
}
.img-circle-sm:hover{
  cursor: pointer;    
}
</style>