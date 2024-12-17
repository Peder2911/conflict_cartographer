<template>
   <Card :loaded="loaded">
      <template v-slot:header>
         <h1>MENU</h1>
      </template>
      <template v-slot:content>
         <div id="content-holder">
            <div id="profile-pic-holder">
               <account-box :size="200"></account-box>
            </div>
            <div id="menu-content-container">
               <div id="menu-links">
                  <button title="Add new predictions"
                    v-on:click="$router.push('/')"
                    v-if="is_open">
                     <checkbox-multiple-marked :size="30"></checkbox-multiple-marked>
                     Participate
                  </button>
                  <button title="View evaluation"
                     v-on:click="$router.push('/results/-2/')">
                     <scale-balance :size="30"></scale-balance>
                     Evaluation
                  </button>
                  <button title="Change assigned countries"
                     v-on:click="$router.push('/assign')">
                     <map-plus :size="30"></map-plus>
                     Countries
                  </button>
                  <button title="Edit profile information"
                     v-on:click="$router.push('/questionaire')">
                     <account-edit :size="30"></account-edit>
                     Profile
                  </button>
                  <button v-on:click="$router.push('deleteme')">
                     <account-cancel :size="30"></account-cancel>
                     Delete me
                  </button>
               </div>
               <div class="menu-body" v-if="is_open">
                  <p v-if="pred_period_start!='' && pred_period_end!=''">
                     You are currently predicting for {{ pred_period_start }} - {{ pred_period_end }}:
                  </p>
                  <CountryStatusTable v-if="assigned != undefined" :countries="assigned"></CountryStatusTable>
               </div>
               <div class="menu-body" v-else>
                  <p v-if="part_period_start != ''">
                     We are currently not accepting predictions. Check back 1st. {{ part_period_start }}, or
                     click "Evaluation" to see how you did last prediction period.
                  </p>
               </div>
            </div>
         </div>
      </template>
      <template v-slot:footer>
         <div class="footer-buttons">
            <button title="Add new predictions"
               v-if="is_open && unfulfilled" v-on:click="$router.push('/')" 
               id="participate-button" class="progress">
               Participate
            </button>
            <button title="View evaluation"
               v-else v-on:click="$router.push('results')" 
               id="eval-button" class="alt">
               Evaluation
            </button>
         </div>
      </template>
   </Card>
</template>
<style lang="sass" scoped>
@import "@/sass/variables"

.menu-body
   width: 100%
   display: grid

#participate-button
   background-color: $ui-highlight

#eval-button
   background-color: $ui-progress-alt

#profile-pic-holder
   display: grid
   place-items: center

#menu-content-container
   display: grid
   grid-gap: 20px
   padding: 0 20px

#menu-links
   display: grid
   grid-auto-flow: column
   grid-gap: 10px
   place-items: left 
   grid-template-columns: repeat(auto-fit, minmax(80px,1fr))

#menu-links button
   display: grid
   background: $ui-darkgray
   padding: 20px 0
   height: 90px
   //width: 100px 
   font-size: 15px
</style>
<script>
import Card from "@/components/Card"
import CountryStatusTable from "@/components/CountryStatusTable"
import {format_date} from "@/date_formatting"

import AccountBox from "vue-material-design-icons/AccountBox"
import AccountEdit from "vue-material-design-icons/AccountEdit"

import MapPlus from "vue-material-design-icons/MapPlus"
import CheckboxMultipleMarked from "vue-material-design-icons/CheckboxMultipleMarked"
import ScaleBalance from "vue-material-design-icons/ScaleBalance"
import AccountCancel from "vue-material-design-icons/AccountCancel"
export default {
   components: {
      Card,
      AccountBox,
      AccountEdit,
      MapPlus,
      CheckboxMultipleMarked,
      ScaleBalance,
      CountryStatusTable,
      AccountCancel,
   },
   computed:{
      loaded(){
         return this.unfulfilled !== undefined && 
            this.is_open !== undefined &&
            this.username !== undefined
      }
   },
   data(){
      return {
         is_open: undefined,
         unfulfilled: undefined,
         username: undefined,
         part_period_start:"",
         pred_period_start: "",
         pred_period_end: "",
         assigned:undefined
      }
   },
   methods:{
      check_open(){
         this.$api.get.rel("period/open")
            .then((r)=>{
               this.is_open = r.data.open
            })
      },
      check_fulfilled(){
         this.$api.get.rel("profile/unfulfilled")
            .then((r)=>{
               this.unfulfilled = r.data.countries.length > 0
            })
      },
      fetch_username(){
         this.$api.get.rel("profile/whoami")
            .then((r)=>{
               this.username = r.data.name
            })
      },

      get_assigned(){
         this.$api.get.rel("profile/assigned")
            .then((r)=>{
               this.assigned = r.data.countries
            })
      },
      get_next_pred_period(){
         this.$api.get.rel("period/current")
            .then((r)=>{
               this.part_period_start = format_date(r.data.end)
            })
      },
      get_pred_period(){
         this.$api.get.rel("period/next")
            .then((r)=>{
               this.pred_period_start = format_date(r.data.start)
               this.pred_period_end = format_date(r.data.end)
            })
      },
   },
   mounted(){
      this.check_open()
      this.check_fulfilled()
      this.fetch_username()
      this.get_next_pred_period()
      this.get_assigned()
      this.get_pred_period()
   }
}
</script>
