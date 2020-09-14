import Vue from 'vue'
import VueRouter from 'vue-router'
import Home from '../views/Home.vue'
import MapTest from '../views/MapTest.vue'
import MapMain from '../views/MapMain.vue'
import SelectLocation from '../views/SelectLocation.vue'
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
    path: '/map',
    name: 'Map',
    component: MapMain
  },
  {
    path: '/selectlocation',
    name: 'SelectLocation',
    component: SelectLocation
  },

]

const router = new VueRouter({
  mode: 'history',
  base: process.env.BASE_URL,
  routes
})

export default router
