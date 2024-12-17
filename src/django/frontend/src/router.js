
import VueRouter from "vue-router"
import Vue from "vue"

import LoadingRouter from "@/components/LoadingRouter"
import CountryAssign from "@/components/CountryAssign"
import MapEditor from "@/components/MapEditor"
import ProgressMenu from "@/components/ProgressMenu"
import MetaQuestionaire from "@/components/MetaQuestionaire"
import ProjectInfo from "@/components/ProjectInfo"
import StatusScreen from "@/components/StatusScreen"
import Closed from "@/components/Closed"

import Menu from "@/views/Menu"
import Results from "@/views/Results"
import ResultsMap from "@/views/ResultsMap"
import Deleteme from "@/views/Deleteme"

Vue.use(VueRouter)

const routes = [
   {path: "/",component: LoadingRouter,name:"Loading"},
   {path: "/assign",component: CountryAssign,name:"Assign"},
   {path: "/ctry/:gwno",component: MapEditor,name:"Editor"},
   {path: "/questionaire",component: MetaQuestionaire,name:"Questionaire"},
   {path: "/menu",component: Menu,name:"Menu"},
   {path: "/results/:shift",component: Results,name:"Results"},
   {path: "/results/:shift/map/:gwno",component: ResultsMap,name:"ResultsMap"},
   {path: "/progress",component: ProgressMenu,name:"Progress"},
   {path: "/info",component: ProjectInfo,name:"Info"},
   {path: "/status",component: StatusScreen,name:"Status"},
   {path: "/closed",component: Closed,name:"Closed"},
   {path: "/deleteme",component: Deleteme,name:"Deleteme"},
]

const router = new VueRouter({
   routes
})

export default router
