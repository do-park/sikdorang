<template>
  <div>
    <div class="img-wrap">
      <img v-if="getUserInfo.profile_image" class="user-profile-img" :src="imgSrc" alt="user profile image">
      <img v-else class="user-profile-img" src="../../assets/userDefault.png" alt="user profile image">
    </div>
    <i @click="callImgChangeBtn()" class="camera fas fa-camera fa-1x"></i>
    <div class="input-wrap">
      <input @change="fileChange" type="file" ref="userImage" class="img-change-btn" id="user-image" accept=".jpg, .jpeg, .gif">
    </div>
    <div class="username">{{ getUserInfo.username }}</div>
    <AchievementBadge/>
  </div>
</template>

<script>
import { mapGetters } from "vuex"
import AchievementBadge from './AchievementBadge'
const mypage = "mypage"

export default {
  name: "userProfile",
  components : {
    AchievementBadge,
  },
  data() {
    return {
      userImage: null,
    }
  },
  computed: {
    ...mapGetters(mypage, [
      'getUserInfo'
    ]),
    imgSrc() {
        return this.getUserInfo.profile_image
    }
  },
  methods: {
    callImgChangeBtn() {
      var myinput = document.getElementById('user-image')
      myinput.click()
    },
    fileChange(e) {
      this.userImage = this.$refs.userImage.files[0]
      this.imageSubmit(e)
    },
    imageSubmit(e) {
        console.log(e)
        const requestHeaders = {
            headers: {
                Authorization: `JWT ${this.$cookies.get("auth-token")}`,
                'Content-Type' : 'multipart/form-data',
            }
        }
        let fd = new FormData()
        fd.append('profile_image', this.userImage)
        fd.append('username', this.getUserInfo.username)
        this.$axios
        .put('/rest-auth/user/', fd, requestHeaders)
        .then(res => {
            console.log(res)
            alert('변경이 완료되었습니다.')
        })
        .catch(err => console.error(err))
    }


  },
}
</script>

<style scoped>
.user-profile-img {
  display: block;
  width: 7rem;
  height: 7rem;
  border-radius: 50%;
  margin: auto;

  background-repeat: no-repeat;
  background-position: center center;
  background-size: cover;
} 
.img-wrap {
  margin: 10px 0px 5px;
}
.camera {
  position: relative;
  border-radius: 50%;
  padding: 0.5rem;
  border: 1px black solid;
  background-color: white;
  left: 55%;
  top: -2.4rem;
  cursor: pointer;
}
.input-wrap {
  display: none;
}


.username {
  font-size: 22px;
  text-align: center;
  margin-top: -1.5rem;
}

</style>