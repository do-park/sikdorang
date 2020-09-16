import Vue from "vue";
import App from "./App.vue";
import router from "./router";
import store from "./store";
import VueCookies from 'vue-cookies'
import vuetify from "./plugins/vuetify";
import axios from "axios";

Vue.prototype.$axios = axios;
axios.defaults.baseURL = "http://localhost:8080";

Vue.config.productionTip = false;
Vue.use(VueCookies)

new Vue({
  router,
  store,
  vuetify,
  render: (h) => h(App),
}).$mount("#app");
