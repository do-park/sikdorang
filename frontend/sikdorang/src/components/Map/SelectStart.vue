<template>
  <div>
    <div class="text-center">
      <hr />
      <div class="top-place"><truck /></div>
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
        <!-- <button class="btn btn-primary m-3 go-btn" @click="search">
          다른 지역으로 갈래요!
        </button> -->
        <input
          type="button"
          @click="sample3_execDaumPostcode()"
          value="다른 지역으로 갈래요!"
        /><br />
        <div
          id="wrap"
          style="
            display: none;
            border: 1px solid;
            width: 500px;
            height: 300px;
            margin: 5px 0;
            position: relative;
          "
        >
          <img
            src="//t1.daumcdn.net/postcode/resource/images/close.png"
            id="btnFoldWrap"
            style="
              cursor: pointer;
              position: absolute;
              right: 0px;
              top: -1px;
              z-index: 1;
            "
            @click="foldDaumPostcode()"
            alt="접기 버튼"
          />
        </div>
      </div>
      <hr />
    </div>
  </div>
</template>

<script>
import Swal from "sweetalert2";
import truck from "./truck.vue";

export default {
  name: "SelectStart",
  components: {
    truck,
  },
  data() {
    return {
      Latitude: null,
      Longitude: null,
      dialog: false,
      destination: "",
      message: "",
      element_wrap: null,
    };
  },
  mounted() {
    const script = document.createElement("script"); // 지우면 작동안함
    /* global daum */ script.src =
      "https://t1.daumcdn.net/mapjsapi/bundle/postcode/prod/postcode.v2.js";
    document.head.appendChild(script);
    this.element_wrap = document.getElementById("wrap");
  },
  methods: {
    foldDaumPostcode() {
      // iframe을 넣은 element를 안보이게 한다.
      this.element_wrap.style.display = "none";
    },
    sample3_execDaumPostcode() {
      const self = this;
      // 현재 scroll 위치를 저장해놓는다.
      var currentScroll = Math.max(
        document.body.scrollTop,
        document.documentElement.scrollTop
      );
      new daum.Postcode({
        oncomplete: function (data) {
          // 검색결과 항목을 클릭했을때 실행할 코드를 작성하는 부분.

          // 각 주소의 노출 규칙에 따라 주소를 조합한다.
          // 내려오는 변수가 값이 없는 경우엔 공백('')값을 가지므로, 이를 참고하여 분기 한다.
          var addr = ""; // 주소 변수
          var extraAddr = ""; // 참고항목 변수

          //사용자가 선택한 주소 타입에 따라 해당 주소 값을 가져온다.
          if (data.userSelectedType === "R") {
            // 사용자가 도로명 주소를 선택했을 경우
            addr = data.roadAddress;
          } else {
            // 사용자가 지번 주소를 선택했을 경우(J)
            addr = data.jibunAddress;
          }

          // 사용자가 선택한 주소가 도로명 타입일때 참고항목을 조합한다.
          if (data.userSelectedType === "R") {
            // 법정동명이 있을 경우 추가한다. (법정리는 제외)
            // 법정동의 경우 마지막 문자가 "동/로/가"로 끝난다.
            if (data.bname !== "" && /[동|로|가]$/g.test(data.bname)) {
              extraAddr += data.bname;
            }
            // 건물명이 있고, 공동주택일 경우 추가한다.
            if (data.buildingName !== "" && data.apartment === "Y") {
              extraAddr +=
                extraAddr !== "" ? ", " + data.buildingName : data.buildingName;
            }
            // 표시할 참고항목이 있을 경우, 괄호까지 추가한 최종 문자열을 만든다.
            if (extraAddr !== "") {
              extraAddr = " (" + extraAddr + ")";
            }
            // 조합된 참고항목을 해당 필드에 넣는다.
          }

          // 우편번호와 주소 정보를 해당 필드에 넣는다.
          Swal.fire({
            html: `${addr}` + "에서 시작해볼까요?",
            confirmButtonColor: "crimson",
          }).then((res) => {
            if (res) {
              console.log(res, "ok눌렀다");
              self.$cookies.set("searchMethod", "Regions");
              self.$cookies.set("destination", addr);
              self.destination = "";
              self.$emit("flag", false);
            }
          });

          // iframe을 넣은 element를 안보이게 한다.
          // (autoClose:false 기능을 이용한다면, 아래 코드를 제거해야 화면에서 사라지지 않는다.)
          self.element_wrap.style.display = "none";

          // 우편번호 찾기 화면이 보이기 이전으로 scroll 위치를 되돌린다.
          document.body.scrollTop = currentScroll;
        },
        // 우편번호 찾기 화면 크기가 조정되었을때 실행할 코드를 작성하는 부분. iframe을 넣은 element의 높이값을 조정한다.
        onresize: function (size) {
          self.element_wrap.style.height = size.height + "px";
        },
        width: "100%",
        height: "100%",
      }).embed(this.element_wrap);

      // iframe을 넣은 element를 보이게 한다.
      this.element_wrap.style.display = "block";
    },
    search() {
      Swal.fire({
        title: "어느 지역을 검색하시겠습니까?",
        input: "text",
        confirmButtonColor: "crimson",
        inputValidator: (value) => {
          if (!value) {
            return "검색어를 입력해주세요.";
          }
        },
      }).then((result) => {
        if (result.value) {
          //empty
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
            //시작 위도,경도 쿠키에 올리기
            this.$cookies.set("startLatitude", this.Latitude);
            this.$cookies.set("startLongitude", this.Longitude);
            this.$cookies.set("searchMethod", "myLocation");
            this.$emit("flag", false);
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
.swal2-popup {
  font-family: "NIXGONM-Vb";
  font-size: 0.7rem !important;
}
</style>
