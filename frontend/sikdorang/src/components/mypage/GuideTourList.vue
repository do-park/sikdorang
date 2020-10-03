<template>
  <div v-if="guideTourList">
    <div v-for="tour in tourList" :key="tour.id">
      <GuideTourListItem :tour="tour" />
    </div>
  </div>
</template>

<script>
import GuideTourListItem from './GuideTourListItem.vue'

export default {
  name: 'GuideTourList',
  components: {
    GuideTourListItem,
  },
  props : {
    guideTourList : Boolean,
  },
  data() {
    return {
      tourList: [],
    }
  },
  mounted() {
    this.getData()
  },
  methods: {
    getData() {
      // auth-token 헤더로 보내서 결제한 가이드 투어 리스트 가져오기
      const requestHeaders = {
        headers: {
          Authorization: `JWT ${this.$cookies.get("auth-token")}`,
        },
      };
      this.$axios
      .get("/guide/paidtour", requestHeaders)
      .then((res) => {
        res.data.forEach((target, index) => {
          const stringDate = target.start_date.toString()
          res.data[index].start_date = `${stringDate.substr(0,4)}-${stringDate.substr(4,2)}-${stringDate.substr(6,2)}`
          const stringDate2 = target.end_date.toString()
          res.data[index].end_date = `${stringDate2.substr(0,4)}-${stringDate2.substr(4,2)}-${stringDate2.substr(6,2)}`
          console.log('디스',this.$store.state.IMG_SERVER_URL + res.data[index].title_img)
          res.data[index].title_img = this.$store.state.IMG_SERVER_URL + res.data[index].title_img
        })
        this.tourList = res.data
      })
      .catch((err) => {
        console.log(err)
      });
    }
  },

}
</script>

<style>

</style>