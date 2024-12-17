
<template>
   <Card :loaded="loaded">
      <template v-slot:header><h1>SUMMARY</h1></template>
      <template v-slot:content>
         <div id="thanks-text">

            <h1>
            Thank you for submitting predictions! 
            </h1>

            <p>
               If you don't want to revise your predictions, you can now close the
               browser window. You have submitted predictions for the period 
               {{start_pred}} - {{end_pred}} for:
            </p>

            <CountryStatusTable :countries="submitted">
            </CountryStatusTable>

            <p>
               The next data-entry period starts {{ next_data_entry }}, 
               where you will predict for conflict in the
               period {{ next_pred_period_start }} - {{ next_pred_period_end }}. 
            </p>

         </div>
      </template>
      <template v-slot:footer>
         <div class="footer-buttons">
            <button title="Go to home menu"
               v-on:click="$router.push('Menu')" class="continue">Menu</button>
            <button title="Change assigned countries"
               v-on:click="to_change_assigned" class="alt">Change assigned</button>
         </div>
      </template>
   </Card>
</template>
<style lang="sass" scoped>
#thanks-text
   padding: 20px

#country-status-table
   width: 100%
</style>
<script>
import Card from "@/components/Card"
import CountryStatusTable from "@/components/CountryStatusTable"
import {format_date} from "@/date_formatting"
export default {
   components: {Card,CountryStatusTable},

   data(){
      return {
         start_pred: "",
         end_pred: "",
         submitted: null,

         next_pred_period_start: "",
         next_pred_period_end: "",

         next_data_entry_start: "",
         next_data_entry_end: "",
      }
   },
      
   computed:{
      loaded(){
         return this.start_pred!=="" && 
            this.end_pred!=="" && 
            this.submitted!==null &&
            this.next_pred_period_start !== "" &&
            this.next_pred_period_end !== "" &&
            this.next_data_entry !== ""
      },
   },

   mounted(){
      this.$api.get.rel("period/next")
         .then((r)=>{
            this.start_pred = format_date(r.data.start)
            this.end_pred = format_date(r.data.end)

            this.next_data_entry = format_date(r.data.start)

         })
         .catch((e)=>{
            console.error(e)
         })
      this.$api.get.rel("profile/assigned")
         .then((r)=>{
            this.submitted = r.data.countries
         })
         .catch((e)=>{
            console.error(e)
         })
      this.$api.get.rel("period/next/2")
         .then((r)=>{
            this.next_pred_period_start = format_date(r.data.start)
            this.next_pred_period_end = format_date(r.data.end)
         })
   },
   methods: {
      to_change_assigned(){
         this.$router.push("/assign")
      }
   }
}
</script>
