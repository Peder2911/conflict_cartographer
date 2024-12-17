import Vue from 'vue'

import "leaflet/dist/leaflet.css"
import "leaflet-draw/dist/leaflet.draw.css"
import Router from "@/router"
import VueCookies from "vue-cookies"

import Api from "@/api"

// Leaflet fixing
import {Icon} from "leaflet"
delete Icon.Default.prototype._getIconUrl;
Icon.Default.mergeOptions({
  iconRetinaUrl: require("leaflet/dist/images/marker-icon-2x.png"),
  iconUrl: require("leaflet/dist/images/marker-icon.png"),
  shadowUrl: require("leaflet/dist/images/marker-shadow.png")
});

Vue.use(VueCookies)

// API setup
let csrf_token = Vue.cookies.get("csrftoken")
Vue.prototype.$api = new Api(csrf_token,"/api")

let app = document.querySelector("#app")
let rv = document.createElement("router-view")
app.appendChild(rv)

new Vue({
   router:Router,
}).$mount('#app')
