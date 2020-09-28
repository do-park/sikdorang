import Vue from "vue"
import App from "./App.vue"
import router from "./router"
import store from "./store"
import VueCookies from "vue-cookies"
import { BootstrapVue, IconsPlugin } from "bootstrap-vue"
// import vuetify from "./plugins/vuetify";
import axios from "axios"
import "bootstrap/dist/css/bootstrap.min.css"
import "bootstrap/dist/js/bootstrap.min.js"
// import swal from 'sweetalert';

Vue.prototype.$axios = axios
// axios.defaults.baseURL = "http://j3d202.p.ssafy.io:8080/"
axios.defaults.baseURL = "http://127.0.0.1:8080/"

Vue.config.productionTip = false
Vue.use(VueCookies)
Vue.use(BootstrapVue)
Vue.use(IconsPlugin)
// Vue.use(swal)

new Vue({
  router,
  store,
  // vuetify,
  render: (h) => h(App),
}).$mount("#app")
