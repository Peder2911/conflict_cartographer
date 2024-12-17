<template>
   <div class="loader-container">
      <div class="content-container" v-if="loaded">
         <div class="time-selector-container">
            Quarter: 
            <input type="number" v-model="shift"> 
            {{ current_partition.start }} - {{ current_partition.end }}
         </div>
         <div class="data-entry-container">
            <table class="selection-table">
               <tr>
                  <th>Name</th>
                  <th>Participants</th>
                  <th>Shapes</th>
                  <th>
                     <button v-on:click="select_all">Select all</button>
                  </th>
               </tr>
               <tr v-for="country in available_countries" :key="country.gwno">
                  <td>{{ country.name }}</td>
                  <td>{{ country.participants }}</td>
                  <td>{{ country.predictions }}</td>
                  <td>
                     <input v-model="country.selected" type="checkbox">
                  </td>
               </tr>
            </table>
            <div>
               <textarea v-model="email_text" type="text">
               </textarea>
               <div class="submit-button-container">
                  <div class="grid-row">
                     <button v-on:click="submit" class="submit-button highlight clickable big">Send</button>
                     <button v-on:click="preview_email" class="submit-button clickable big">Preview</button>
                  </div>
                  You have selected {{ selected_users }} participants ({{ number_of_users }} total)
               </div>
            </div>
         </div>
      </div>

      <div class="loading-screen" v-else>
         Loading participation data...
      </div>

      <modal v-if="show_preview" v-on:closeme="close_modal">
         <div v-html="preview_html"></div>
      </modal>
      
      <transition name="fade">
         <div v-if="working" class="modal-root">
            Working...
         </div>
      </transition>
   </div>
</template>

<style lang="sass" scoped>
@import "/sass/variables.sass"
@import "/sass/style.sass"
@import "/sass/animations.sass"

.loader-container
   display: grid
   place-items: center

.data-entry-container
   display:               grid
   grid-auto-flow:        column
   grid-template-columns: 1fr 1fr
   grid-gap:              $gap 
   height: 90vh
   width: 80vw

.data-entry-container>div
   display: grid

.data-entry-container>div:nth-child(2)
   grid-template-rows: 1fr 100px

.submit-button-container
   height: 100%
   display: grid
   grid-template-rows: 4fr 1fr

.data-entry-container table 
   border-collapse: collapse
   width: 100%

.data-entry-container tr>* 
   padding:     3px $gap 

.data-entry-container table>tr 
   background-color: #ddd

.data-entry-container table>tr:nth-child(even) 
   background-color: white

.data-entry-container table th 
   text-align: left
</style>

<script lang="js">
import * as Axios from "axios"
import Modal from "../components/Modal.vue"
import {DEFAULT_EMAIL_MESSAGE} from "../constants.js"

export default {
   name: "email-interface",
   components: {Modal},
   data() {
      return {
         shift:               null,
         number_of_users:     null,
         current_partition:   null,
         loaded:              false,
         available_countries: [],
         email_text:          DEFAULT_EMAIL_MESSAGE,
         show_preview:        false,
         working:             false
      }
   },
   methods: {
      submit(){
         let data = {
            shift: this.shift,
            countries: this.selected_countries.map(c=>c.gwno),
            content: this.email_text,
            template: -1
         }
         this.working = true
         console.log(this.working)
         Axios.post(this.$public_url("/api/email/send/participants/"), JSON.stringify(data), {headers: {"Content-Type":"application/json"}})
            .then((r)=>{
               this.selected_countries.forEach(ctry => ctry.selected = false)
               this.email_text = DEFAULT_EMAIL_MESSAGE
               this.working = false 
            })
      },
      select_all(){
         this.available_countries.forEach(ctry => ctry.selected = true)
      },
      close_modal(){
         this.show_preview = false 
      },
      preview_email(){
         let data = {
            email: "example@example.com",
            content: this.email_text,
            template: -1,
         }
         Axios.post(this.$public_url("/api/email/preview/"), JSON.stringify(data), {
            headers: {"Content-Type":"application/json"},
            transformResponse: (r)=>r})
            .then((r)=>{
               this.preview_html = r.data
               this.show_preview = true
            })
            .catch((e)=>{
               this.preview_html = `<p>Something went wrong! ${e}`
               this.show_preview = true
            })
      }
   },

   computed: {
      selected_countries(){
         return this.available_countries.filter(c => c.selected) 
      },
      selected_users (){
         return this.selected_countries
            .map(c=>c.participants)
            .reduce((a,b)=> a+b, 0)
      },
   },

   watch: {
      shift: function(val) {
         this.loaded              = false
         this.available_countries = []
         this.current_partition   = null
         this.number_of_users     = null
         Axios.get(this.$public_url(`/api/participation/?shift=${val}`))
            .then((r)=>{
               if(this.shift == val){
                  this.number_of_users     = r.data.number_of_users
                  this.current_partition   = r.data.partition
                  this.loaded              = true

                  let countries = r.data.countries.map(ctry => {
                     return {...ctry, ...{selected: false}}
                  })
                  countries.sort((a,b)=> a.name > b.name)
                  this.available_countries = countries
               }
            })
      },
   },
   mounted(){
      this.shift = -1 
   },
}
</script>
