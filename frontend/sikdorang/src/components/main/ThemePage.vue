<template>
  <div>
      
      <div v-for="theme in themes" :key="theme.id" class="d-flex">
          <!-- <img class="img-circle" :src="require(`../../../public/icons/${theme.id}`)"> -->
          <div class="box">{{theme.theme_name}}</div>
      </div>
  </div>
</template>

<script>
import { mapGetters } from "vuex"
const theme = "theme"

export default {
    name : 'ThemePage',
    data() {
        return{
            themes : this.getThemes
        }
    },
    computed : {
        ...mapGetters(theme, [
            'getThemes'
        ])
    }
}
</script>

<style scoped>
.box{
    background-color: blanchedalmond;
    height : 100px;
}
.img-circle {
  display: inline-block;
  width: 100px;
  height: 100px;
  border-radius: 50%;
  border : 2px solid rgba(242, 157, 143);

  background-repeat: no-repeat;
  background-position: center center;
  background-size: cover;
}

</style>