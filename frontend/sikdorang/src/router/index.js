import Vue from 'vue'
import VueRouter from 'vue-router'
import Home from '../views/Home.vue'
import MapTest from '../views/MapTest.vue'
import Signup from '../views/Signup.vue'
import MapMain from '../views/MapMain.vue'
import IdealTagCupView from '../views/idealtagcup/IdealTagCupView.vue'
import MyPageView from '../views/mypage/MyPageView.vue'

Vue.use(VueRouter)

  const routes = [
  {
    path: '/',
    name: 'Home',
    component: Home
  },
  {
    path: '/maptest',
    name: 'MapTest',
    component: MapTest
  },
  {
    path: '/signup',
    name: 'Signup',
    component: Signup
  },
  {
    path: '/map',
    name: 'MapMain',
    component: MapMain
  },
  {
    path: '/idealtagcup',
    name: 'IdealTagCup',
    component: IdealTagCupView,
  },
  {
    path: '/mypage',
    name: 'MyPageView',
    component: MyPageView,
  }
]

const router = new VueRouter({
  mode: 'history',
  base: process.env.BASE_URL,
  routes
})

export default router
