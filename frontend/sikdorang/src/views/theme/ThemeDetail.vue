<template>
  <div>
    <h3 class="text-center my-3">명예의 전당 [ {{ theme_name }} ] 편</h3>
    <div class="container">
      <div class="row text-center mx-1">
        <div
          @click="goDetail(restuarant)"
          v-for="restuarant in restaurants"
          :key="restuarant.id"
          class="box col-6 m-0 p-1"
        >
          <span v-if="storeClear[restuarant.id] === 1" class="effect">
            <div
              class="img-card"
              :style="getCardBgImage(`${IMG_URL}${restuarant.image}`)"
            >
              <p class="store_name">
                {{ restuarant.store_name }}
              </p>
            </div>
          </span>
          <span v-else>
            <div
              class="img-card"
              :style="getCardBgImage(`${IMG_URL}${restuarant.image}`)"
            >
              <p class="store_name">{{ restuarant.store_name }}</p>
            </div>
          </span>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { mapGetters, mapActions } from "vuex";
const themes = "themes";
import Swal from "sweetalert2";

export default {
  name: "ThemeDetail",
  data() {
    return {
      themeClear: [],
      storeClear: [],
      theme_name: this.$cookies.get("theme_name"),
      theme_id: this.$cookies.get("theme_id"),
      restaurants: [],
      IMG_URL: "http://j3d202.p.ssafy.io:8080",
      file : null,
    };
  },
  created() {
    this.getRestarants();
    this.themeClear = this.getThemesClear;
    this.storeClear = this.getStoreClear;
  },
  computed: {
    ...mapGetters(themes, ["getThemesClear", "getStoreClear"]),
  },
  methods: {
    ...mapActions(themes, ["actionThemesClear", "actionStoreClear"]),
    getCardBgImage(image_url) {
      return 'background-image: url("' + image_url + '")';
    },
    getRestarants() {
      this.$axios
        .get(`/achievement/${this.theme_id}`)
        .then((res) => {
          var restaurants = res.data;
          this.restaurants = restaurants;
        })
        .catch((err) => {
          console.log(err);
        });
    },
    goDetail(rest) {
      console.log(rest);
      if (this.storeClear[rest.id] === 1) {
        
        Swal.fire({
          title: rest.store_name,
          html:
            rest.address +
            "<br />" +
            rest.tel +
            "<br /><br />" +
            rest.description,
          confirmButtonColor: "#d33",
          confirmButtonText: "닫기",
        
        })
      }
      else {
        Swal.fire({
          title: rest.store_name,
          html:
            rest.address +
            "<br />" +
            rest.tel +
            "<br /><br />" +
            rest.description,
          showCancelButton: true,
          confirmButtonColor: "#3085d6",
          cancelButtonColor: "#d33",
          confirmButtonText: "방문하기",
          cancelButtonText: "닫기",
        })
      
      .then((result) => {
        if (result.isConfirmed) {
         Swal.fire({
            title: "영수증 업로드",
            text: "방문 인증을 위한 영수증을 업로드하세요.",
            input: "file",
            inputAttributes: {
              accept: "image/*",
              "aria-label": "Upload your profile picture",
            },
          }).then((file) => {
 
            this.file = file.value;
            // 파일 업로드 부터         
            if (file.value) {
              const receipt_image = file.value
              const reader = new FileReader();
              reader.onload = (e) => {
                Swal.fire({
                  title: "영수증을 업로드합니다.",
                  imageUrl: e.target.result,
                  imageAlt: "영수증을 업로드합니다.",
                  }).then((result) => {
                      if (result) {
                        const requestHeaders = {
                          headers: {
                            Authorization: `JWT ${this.$cookies.get("auth-token")}`,
                            'Content-Type' : 'multipart/form-data',
                          },
                        };
                        //이미지 form
                        let data = new FormData()

                        //이미지와 음식점 이름 넣기
                        data.append('receipt',receipt_image)
                        data.append('rest_name',rest.store_name)
                        
                        this.$axios
                          .post(
                            `achievement/visit_create/${rest.id}`,
                            data,
                            //null대신에 이미지 담아서 전송 -> 백에서 받아서 저장 + 알고리즘 돌리고 결과값 다시 여기로 보냄 
                            requestHeaders
                          )
                          .then((res) => {
                            console.log(res)
                            if (res.data === 1) {
                              this.$set(this.storeClear, rest.id, 1);
                              this.actionStoreClear(this.storeClear);
                              //방문 변경 새로고침하는 함수
                              this.updateClear(rest.id);

                              Swal.fire("Yummy!", "방문 완료!", "success");

                            }
                            else if(res.data === -1) {
                              Swal.fire("Fail", "방문 인증 실패!", "warning");
                            }
                          })
                          .catch((err) => {
                            console.log(err);
                          });
                      }
                  })
              }
              reader.readAsDataURL(file.value);
            }
          })
        }
        
      })
      }
    },
    updateClear(restId) {
      const theme = parseInt(restId / 10);
      let clear = true;
      if (theme <= 7) {
        for (let i = 1; i < 10; i++) {
          if (this.storeClear[theme * 10 + i] != 1) {
            clear = false;
            break;
          }
        }
      } else if ((theme === 8) | (theme === 11)) {
        for (let i = 1; i < 7; i++) {
          if (this.storeClear[theme * 10 + i] != 1) {
            clear = false;
            break;
          }
        }
      } else if (theme === 9) {
        for (let i = 1; i < 9; i++) {
          if (this.storeClear[theme * 10 + i] != 1) {
            clear = false;
            break;
          }
        }
      } else {
        for (let i = 1; i < 8; i++) {
          if (this.storeClear[theme * 10 + i] != 1) {
            clear = false;
            break;
          }
        }
      }
      if (clear === true) {
        const requestHeaders = {
          headers: {
            Authorization: `JWT ${this.$cookies.get("auth-token")}`,
          },
        };
        this.$axios
          .post(`achievement/theme_create/${theme}`, null, requestHeaders)
          .then(() => {
            this.$set(this.themeClear, theme, 1);
            this.actionThemesClear(this.themeClear);
          })
          .catch((err) => {
            console.log(err);
          });
      }
    },
  },
};
</script>

<style scoped>
.box {
  width: 100%;
  /* height: 30vh; */
  padding-bottom: 100%;
}
.img-card {
  width: 100%;
  /* height: 30vh; */
  padding-bottom: 100%;
  background-size: cover;
}
.store_name {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  text-shadow: -1px 0 blanchedalmond, 0 1px blanchedalmond, 1px 0 blanchedalmond,
    0 -1px blanchedalmond;
  font-size: 5vw;
}
.effect {
  position: relative;
  display: block;
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
  /* box-shadow: 0 1px 3px rgba(0, 0, 0, 0.3); */
}
</style>
