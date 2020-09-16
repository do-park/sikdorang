import Vue from "vue";
import App from "./App.vue";
import router from "./router";
import store from "./store";
import VueCookies from 'vue-cookies'
import { BootstrapVue, IconsPlugin } from 'bootstrap-vue'
// import vuetify from "./plugins/vuetify";
import axios from "axios";

Vue.prototype.$axios = axios;
axios.defaults.baseURL = "http://localhost:8080";

Vue.config.productionTip = false;
Vue.use(VueCookies)
Vue.use(BootstrapVue)
Vue.use(IconsPlugin)

new Vue({
  router,
  store,
  // vuetify,
  render: (h) => h(App),
}).$mount("#app");
