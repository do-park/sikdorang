<template>
      <div class="row text-center m-1">
      <div v-for="theme in themes" :key="theme.id" class="m-1">
          <img @click="goDetail(theme)" class="img-circle" :src="require(`../../../public/icons/${theme.id}.png`)">
          <div>{{theme.theme_name}}</div>
      </div>
    </div>
</template>

<script>
import { mapGetters } from "vuex"
const themes = "themes"

export default {
    name : 'ThemePage',
    data() {
        return{
            themes : [],
        }
    },
    computed : {
        ...mapGetters(themes, [
            'getThemes'
        ])
    },
    mounted() {
        this.themes = this.getThemes
        // console.log(this.themes)
    },
    methods : {
        goDetail(theme) {
            this.$cookies.set('theme_id', theme.id)
            this.$cookies.set('theme_name', theme.theme_name)
            this.$router.push('/themedetail')
        }
    },
}
</script>

<style scoped>
.box{
    background-color: blanchedalmond;
  
}
.img-circle {
  display: inline-block;
  width: 100px;
  height: 100px;
  border-radius: 40%;
  border : 3px solid black;
  background-color: rgba(0, 0, 0, 0.445);
  background-repeat: no-repeat;
  background-position: center center;
  background-size: cover;
}
.img-circle:hover {
    cursor: pointer;

}

</style>