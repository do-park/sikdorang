import Vue from "vue"
import VueRouter from "vue-router"
import store from "../store/index.js"
import Home from "../views/Home.vue"
import Signup from "../views/Signup.vue"
import MapMain from "../views/MapMain.vue"
import IdealTagCupView from "../views/idealtagcup/IdealTagCupView.vue"
import MyPageView from "../views/mypage/MyPageView.vue"
import Schedule from "../views/Schedule.vue"
import Recommend from "../views/Recommend.vue"
import Payment from "../views/pay/Payment.vue"
import Result from "../views/pay/Result.vue"
import ThemeDetail from "../views/theme/ThemeDetail.vue"
import TripScheduleFormView from "../views/travelguide/TripScheduleFormView.vue"
import TripProductDetailView from "../views/tripproduct/TripProductDetailView.vue"
import TripProductsView from "../views/tripproduct/TripProductsView.vue"
import TripProductOrder from "../views/tripproduct/TripProductOrder.vue"
import ReviewForm from "../views/review/ReviewForm.vue"
import SikdorangRecommendView from "../views/recommend/SikdorangRecommendView.vue"
import PartyList from "../views/party/PartyList.vue"
import PartyListItemDetail from "../views/party/PartyListItemDetail.vue"
import PartyForm from "../views/party/PartyForm.vue"
import MessageForm from "../components/message/MessageForm.vue"
import PhoneNumberAuthentication from "../components/authentication/PhoneNumberAuthentication.vue"
import Error404View from "../views/Error404View.vue"

Vue.use(VueRouter)

// const getCookie = function(name) {
//   var value = document.cookie.match('(^|;) ?' + name + '=([^;]*)(;|$)');
//   return value? value[2] : null;
// }


const requireAuth = () => (from, to, next) => {
  if (store.state.isLogin) return next()
  next('/')
}

const requireNotAuth = () => (from, to, next) => {
  if (!store.state.isLogin) return next()
  next('/')
}

const requireTags = () => (from, to, next) => {
  if (store.state.isLogin && store.state.mypage.userInfo.done_cup) return next()
  next('/idealtagcup')
}

const requireNoTags = () => (from, to, next) => {
  if (store.state.mypage.userInfo.done_cup === false) return next()
  next('/')
}

const requireGuide = () => (from, to, next) => {
  if (store.state.mypage.userInfo.user_code === 1) return next()
  next('/mypage')
}

const routes = [
  {
    path: "/",
    name: "Home",
    component: Home,
  },
  {
    path: "/signup",
    name: "Signup",
    component: Signup,
    beforeEnter: requireNotAuth(),
  },
  {
    path: "/map",
    name: "MapMain",
    component: MapMain,
  },
  {
    path: "/idealtagcup",
    name: "IdealTagCup",
    component: IdealTagCupView,
    beforeEnter: requireNoTags(),
  },
  {
    path: "/mypage",
    name: "MyPageView",
    component: MyPageView,
    beforeEnter: requireAuth(),
  },
  {
    path: "/schedule",
    name: "Schedule",
    component: Schedule,
    beforeEnter: requireTags(),
  },
  {
    path: "/recommend",
    name: "Recommend",
    component: Recommend,
    beforeEnter: requireTags(),
  },
  {
    path: "/payment",
    name: "Payment",
    component: Payment,
    // payment에 필요한 데이터가 저장되어 있는지 체크하는 로직 필요
  },
  {
    path: "/result",
    name: "Result",
    component: Result,
    // payment 관련 데이터 체크로직 필요
  },
  {
    path: "/themedetail",
    name: "ThemeDetail",
    component: ThemeDetail,
    // ThmeDetail에서 필요한 데이터 체크로직 필요
  },
  {
    path: "/trip/createchedule",
    name: "TripScheduleFormView",
    component: TripScheduleFormView,
    beforeEnter: requireGuide()
  },
  {
    path: "/trip/detail/:item_pk",
    name: "TripProductDetailView",
    component: TripProductDetailView,
  },
  {
    path: "/trip/list",
    name: "TripProductsView",
    component: TripProductsView,
  },
  {
    path: "/trip/order",
    name: "TripProductOrder",
    component: TripProductOrder,
    // getOrderTrip 체크 필요
  },
  {
    path: "/review/form",
    name: "ReviewForm",
    component: ReviewForm,
    //storeId: this.$cookies.get("review-store-id") 체크, 로그인 체크 필요
  },
  {
    path: "/sikdorang/recommendation",
    name: "SikdorangRecommendView",
    component: SikdorangRecommendView,
    beforeEnter: requireTags()
  },
  {
    path: "/party/list",
    name: "PartyList",
    component: PartyList,
  },
  {
    path: "/party/detail",
    name: "PartyListItemDetail",
    component: PartyListItemDetail,
  },
  {
    path: "/party/form",
    name: "PartyForm",
    component: PartyForm,
    beforeEnter: requireAuth()
  },
  {
    path: "/beguide",
    name: "PhoneNumberAuthentication",
    component: PhoneNumberAuthentication,
    beforeEnter: requireAuth(),
  },
  {
    path: "/message/test",
    name: "MessageForm",
    component: MessageForm,
    // 삭제요청
  },
  //이 라우터는 항상 최하단에 위치해야 합니다.
  {
    path: "*",
    name: "Error404View",
    component:Error404View,
  },
]

const router = new VueRouter({
  mode: "history",
  base: process.env.BASE_URL,
  routes,
})

export default router
