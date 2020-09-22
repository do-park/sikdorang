<template>
  <div>
    <h1>명예의 전당 [ {{theme_name}} ]편 </h1>
    <div class="container">
        <div class="row text-center">
            <div @click="goDetail(restuarant)" v-for="restuarant in restaurants" :key="restuarant.id" class="box col-sm-4 m-0">
                <div class="img-card" :style="getCardBgImage(`${IMG_URL}${restuarant.image}`)">
                    
                    {{restuarant.store_name}}
                </div>
            </div>
        </div>
  </div>
     
  </div>
</template>

<script>
import swal from 'sweetalert'
var BASE_URL = 'http://j3d202.p.ssafy.io:8080'
export default {
    name : "ThemeDetail",
    data() {
        return {
            theme_name : this.$cookies.get('theme_name'),
            theme_id : this.$cookies.get('theme_id'),
            restaurants : [{"id" : 111, "store_name" : "빵집1"},{"id" : 222, "store_name" : "빵집2"},{"id" : 333, "store_name" : "빵집3"}],
            IMG_URL: `${BASE_URL}`
        }
    },
    created() {
      
        this.getRestarants()
    },
    methods : {
       getCardBgImage(image_url){
            return 'background-image: url("' + image_url + '")';
        },
        getRestarants() {
            console.log(this.theme_id)
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
    height : 400px;
    background: blanchedalmond;
}
.img-card{
    /* width : 500px; */
    height : 400px;
}
</style>