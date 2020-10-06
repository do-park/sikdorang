<template>
<div class="con">
  <div v-if="result" id=container>
    <p class="m-0 text-left ml-3">{{ username }}님, </p>
    <div id=flip>
       <div><div>{{result.store_name }}</div></div>
       <div><div>{{second_ment}} 맛집</div></div>
      <div><div>{{ address }}의</div></div>
    </div>
    <p class="text-right mr-3">어떠세요?<i class="far fa-hand-pointer"></i></p>
  </div>

</div>
</template>

<script>
import { mapActions } from 'vuex'
export default {
  name: "Recommend",
  data() {
    return {
      result: null,
      address: null,
      second_ment : '',
      category_name : ["한식","분식","피자","치킨","돈가스/회/일식","카페/디터즈/베이커리","아시안푸드","양식","중식","도시락/샌드위치","패스트푸드","술집","족발/보쌈","찜/탕"]
    };
  },
  props : {
    username : String,
  },
  created() {
    this.getRecommend();
  },
  methods: {
    ...mapActions('sikRec', ['actionForUser']),
    getRecommend() {
      const requestHeaders = {
        headers: {
          Authorization: `JWT ${this.$cookies.get("auth-token")}`,
        },
      };
      this.$axios
        .get("/recommend/coldstart", requestHeaders)
        .then((response) => {
          this.result = response.data;
          this.second_ment = this.category_name[this.result.category]
          this.actionForUser(this.result)
          const temp = this.result.address.split(" ");
          this.address = temp[0] + " " + temp[1];
        })
        .catch((err) => console.error(err));
    },
  },
};
</script>

<style scoped>
/* @import url('https://fonts.googleapis.com/css?family=Roboto:700'); */
.con{
  max-width: 600px;
  width : 100vw;
  height : 20vh;
}
#container {
  color:#999;
  text-transform: uppercase;
  font-size:30px;
  font-weight:bold;
  /* padding-top:200px;   */
  position:fixed;
  width:100%;
  bottom :70%;
  display:block;
}

#flip {
  height:50px;
  overflow:hidden;
}

#flip > div > div {
  color:#fff;
  padding:4px 12px;
  height:50px;
  margin-bottom:45px;
  display:inline-block;
}

#flip div:first-child {
  animation: show 5s linear infinite;
}

#flip div div {
  background:black;
}
#flip div:first-child div {
  background:black;
}
#flip div:last-child div {
  background:black;
}


@keyframes show {
  0% {margin-top:-270px;}
  5% {margin-top:-180px;}
  33% {margin-top:-180px;}
  38% {margin-top:-90px;}
  66% {margin-top:-90px;}
  71% {margin-top:0px;}
  99.99% {margin-top:0px;}
  100% {margin-top:-270px;}
}

.pp {
  position:fixed;
  width:100%;
  bottom:30px;
  font-size:12px;
  color:#999;
  margin-top:200px;
}
 
</style>