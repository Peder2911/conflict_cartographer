
import Vue from "vue"
import VueRouter from "vue-router"
import App from "./App.vue"

import PredictionMap from "./views/PredictionMap.vue"
import ParticipationTimeline from "./views/ParticipationTimeline.vue"
import EmailInterface from "./views/EmailInterface.vue"
import SingleEmailInterface from "./views/SingleEmailInterface.vue"
import LandingPage from "./views/LandingPage.vue"
import Info from "./views/Info"
import EmailStatusManagement from "./views/EmailStatusManagement"

const data_from_backend = JSON.parse(document.querySelector("#data-from-backend").textContent)
console.log(data_from_backend)

const PUBLIC_URL = data_from_backend.public_url?data_from_backend.public_url:""

Vue.prototype.$public_url = (p)=> {
   return `${PUBLIC_URL}${p}`
}

Vue.use(VueRouter)

const routes = [
   {path:"/map", component: PredictionMap},
   {path:"/participation", component: ParticipationTimeline},
   {path:"/email", component: EmailInterface},
   {path:"/single-email", component: SingleEmailInterface},
   {path:"/", component: LandingPage},
   {path:"/info", component: Info},
   {path:"/email-status-management", component: EmailStatusManagement},
]

const router = new VueRouter({routes})

new Vue({
   router,
   render: h => h(App),
}).$mount("#app")
