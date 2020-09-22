import Vue from 'vue'
import VueRouter from 'vue-router'
import Home from '../views/Home.vue'
import MapTest from '../views/MapTest.vue'
import Signup from '../views/Signup.vue'
import MapMain from '../views/MapMain.vue'
import IdealTagCupView from '../views/idealtagcup/IdealTagCupView.vue'
import MyPageView from '../views/mypage/MyPageView.vue'
import Schedule from "../views/Schedule.vue"
import Recommend from "../views/Recommend.vue"
import ApplicationGuideView from "../views/travelguide/ApplicationGuideView.vue"
import Payment from "../views/pay/Payment.vue"
import Result from "../views/pay/Result.vue"
import TripScheduleFormView from "../views/travelguide/TripScheduleFormView.vue"
import TripProductDetailView from "../views/tripproduct/TripProductDetailView.vue"
import TripProductsView from "../views/tripproduct/TripProductsView.vue"

Vue.use(VueRouter)

const routes = [
  {
    path: "/",
    name: "Home",
    component: Home,
  },
  {
    path: "/maptest",
    name: "MapTest",
    component: MapTest,
  },
  {
    path: "/signup",
    name: "Signup",
    component: Signup,
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
  },
  {
    path: '/mypage',
    name: 'MyPageView',
    component: MyPageView,
  },
  {
    path: "/schedule",
    name: "Schedule",
    component: Schedule,
  },
  {
    path: "/recommend",
    name: "Recommend",
    component: Recommend,
  },
  {
    path: "/guide/application",
    name: "ApplicationGuideView",
    component: ApplicationGuideView,
  },
  {
    path: "/payment",
    name: "Payment",
    component: Payment,
  },
  {
    path: "/result",
    name: "Result",
    component: Result,
  },
  {
    path: "/trip/createchedule",
    name: "TripScheduleFormView",
    component: TripScheduleFormView,
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
  }

]

const router = new VueRouter({
  mode: "history",
  base: process.env.BASE_URL,
  routes,
})

export default router
