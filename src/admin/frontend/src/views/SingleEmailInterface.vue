<template>
   <div class="single-email-root">
      <div class="content-container">
         <table class="email-header-table">
            <tr>
               <td>
                  From: 
               </td>
               <td class="input-like">
                  conflictcartographer@prio.org
               </td>
            </tr>
            <tr>
               <td>
                  To: 
               </td>
               <td>
                  <input type="text" v-model="recipient">
               </td>
            </tr>
         </table>
         <textarea v-model="email_text"></textarea>
         <div class="grid-row">
            <button v-on:click="send_email" class="highlight big">Send</button>
            <button v-on:click="preview_email" class="big">Preview</button>
         </div>
      </div>
      <modal v-if="show_preview" v-on:closeme="close_modal">
         <div v-html="preview_html"></div>
      </modal>
      <transition name="fade">
         <div class="modal-root" v-if="working">
            Working...
         </div>
      </transition>
   </div>
</template>
<style lang="sass" scoped>
@import "../sass/style.sass"
@import "../sass/variables.sass"
@import "../sass/animations.sass"

.email-header-table
   width: 100%
   height: 100px

td>input
   width: 100%

tr>td:first-child
   width: 100px

.content-container
   width: 50vw 
   height: 90%
   grid-template-rows: 100px 1fr 60px 

.single-email-root
   display: grid
   place-items: center
   height: 100vh

textarea
   height: 100%

</style>
<script>
import * as Axios from "axios"
import Modal from "../components/Modal.vue"
import {DEFAULT_RECIPIENT, DEFAULT_EMAIL_MESSAGE} from "../constants.js"

export default {
   name: "single-email",
   components: {Modal},
   data(){
      return {
         recipient:    DEFAULT_RECIPIENT,
         email_text:   DEFAULT_EMAIL_MESSAGE,
         preview_html: null,
         show_preview: false,
         working:      false
      }
   },
   methods: {
      close_modal(){
         this.show_preview = false 
      },
      send_email(){
         this.working = true
         let data = {
            email: this.recipient, 
            content: this.email_text,
            template: -1,
         }
         Axios.post(this.$public_url("/api/email/send/single/"), JSON.stringify(data), {headers: {"Content-Type":"application/json"}})
            .then((r)=>{
               this.recipient = DEFAULT_RECIPIENT
               this.email_text = DEFAULT_EMAIL_MESSAGE
               this.working = false 
            })
            .catch((e)=>{
            })
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
   }
}
</script>
