<template>
  <div>
      <h1>명예의 전당 [{{theme_name}}]편</h1>
      <div class="container">
      <div class="row text-center">
      <div @click="goDetail(restuarant)" v-for="restuarant in restaurants" :key="restuarant.id" class="box col-sm-4 m-0">
          <div>
              {{restuarant.store_name}}
          </div>
      </div>
    </div>
  </div>
     
  </div>
</template>

<script>
import swal from 'sweetalert'

export default {
    name : "ThemeDetail",
    data() {
        return {
            theme_name : this.$cookies.get('theme_name'),
            theme_id : this.$cookies.get('theme_id'),
            restaurants : [{"id" : 111, "store_name" : "빵집1"},{"id" : 222, "store_name" : "빵집2"},{"id" : 333, "store_name" : "빵집3"}],
        }
    },
    created() {
        this.showAlert()
        this.getRestarants()
    },
    methods : {
        showAlert() {
            swal("방문한 음식점은 clear로 표시됩니다 ^^.")
        },
        getRestarants() {
            this.$axios.get(`/achievement/${this.theme_id}`)
            .then(res => {
                var restaurants = res.data
                this.restaurants = restaurants
            })
            .catch(err => {
                console.log(err)
            })
        
        },
        goDetail(rest) {
            swal(rest.store_name,rest.description)
        }
    }, 
}
</script>

<style scoped>
.box {
    height : 100px;
    background: blanchedalmond;
}
</style>