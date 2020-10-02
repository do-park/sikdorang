<template>
  <div>
    <div class="text-center">
      <hr />
      <div class="top-place">대충 뭐 들어가는곳</div>
      <hr />
      <div>
        <button
          type="button"
          class="btn btn-primary m-3 go-btn"
          @click="getMyLocation"
        >
          내 위치에서 볼래요!
        </button>
      </div>
      <div>
        <button class="btn btn-primary m-3 go-btn" @click="search">
          다른 지역으로 갈래요!
        </button>
      </div>
      <hr />
    </div>
  </div>
</template>

<script>
import Swal from "sweetalert2";

export default {
  name: "SelectStart",
  data() {
    return {
      Latitude: null,
      Longitude: null,
      dialog: false,
      destination: "",
      message: "",
    };
  },

  methods: {
    search() {
      Swal.fire({
        title: "어느 지역을 검색하시겠습니까?",
        input: "text",
        inputValidator: (value) => {
          if (!value) {
            return "검색어를 입력해주세요.";
          }
        },
      }).then((result) => {
        if (result.value) {
          Swal.fire({
            html: `${result.value}` + "에서 시작해볼까요?",
          }).then((res) => {
            if (res) {
              console.log(res, "ok눌렀다");
              this.$cookies.set("searchMethod", "Regions");
              this.$cookies.set("destination", result.value);
              this.destination = "";
              this.$emit("flag", false);
            }
          });
        }
      });
    },

    getMyLocation() {
      if ("geolocation" in navigator) {
        //위치 요청
        navigator.geolocation.getCurrentPosition(
          function (pos) {
            this.Latitude = pos.coords.latitude;
            this.Longitude = pos.coords.longitude;
            Swal.fire(
              "내 위치",
              this.Latitude + ", " + this.Longitude,
              "success"
            ).then((res) => {
              if (res) {
                //시작 위도,경도 쿠키에 올리기
                this.$cookies.set("startLatitude", this.Latitude);
                this.$cookies.set("startLongitude", this.Longitude);
                // this.$cookies.set('startLatitude',36.0954341)
                // this.$cookies.set('startLongitude',128.4138607)
                this.$cookies.set("searchMethod", "myLocation");
                this.$emit("flag", false);
              }
            });
          }.bind(this)
        );
      } else {
        //위치정보 사용 불가능
        console.log("위치 정보 사용이 불가능합니다.");
      }
    },

    findPath(destination) {
      this.destination = destination;
      this.message = `${destination}에서 시작해볼까요?`;
      this.$cookies.set("destination", destination);
    },
  },
};
</script>

<style>
.top-place {
  height: 300px;
}

.go-btn {
  width: 200px;
}
</style>