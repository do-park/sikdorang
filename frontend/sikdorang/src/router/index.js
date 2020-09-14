import Vue from 'vue'
import VueRouter from 'vue-router'
import Home from '../views/Home.vue'
import MapTest from '../views/MapTest.vue'
import Signup from '../views/Signup.vue'

Vue.use(VueRouter)

  const routes = [
  {
    path: '/',
    name: 'Home',
    component: Home
  },
  {
    path: '/map',
    name: 'MapTest',
    component: MapTest
  },
  {
    path: '/signup',
    name: 'Signup',
    component: Signup
  },

]

const router = new VueRouter({
  mode: 'history',
  base: process.env.BASE_URL,
  routes
})

export default router
