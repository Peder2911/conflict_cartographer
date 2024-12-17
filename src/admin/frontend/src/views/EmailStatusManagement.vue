<template>
   <div>
      <div class="content-container">
         <div>
            <table>
               <tr>
                  <td>
                     Email:
                  </td>
                  <td>
                     <input v-model="selected_email" type="text">
                  </td>
               </tr>
               <tr>
                  <td>
                     Clear last emailed:
                  </td>
                  <td>
                     <input v-model="clear_last_emailed" type="checkbox">
                  </td>
               </tr>
               <tr>
                  <td>
                     Set unsubscribe status:
                  </td>
                  <td>
                     <select v-model="set_subscribe_status">
                        <option value="false">Subscribed</option>
                        <option value="true">Unsubscribed</option>
                     </select>
                  </td>
               </tr>
            </table>
            <button v-on:click="submit">Submit</button>
         </div>
      </div>
      <transition name="fade">
         <div class="modal-root" v-if="working">
            Working...
         </div>
      </transition>
   </div>
</template>
<style lang="sass" scoped>
@import "../sass/variables.sass"
@import "../sass/style.sass"
@import "../sass/animations.sass"

.content-container
   height: 100%
   width: 100%
   place-items: center

.content-container>div:nth-child(1)
   display: grid
   grid-template-rows: 1fr 40px
   place-items: center
   background-color: #f5f5f5
   padding: 20px
   grid-gap: 20px

td
   padding: $gap 

tr
   height: 60px

button
   width: 200px 

</style>
<script>
import {DEFAULT_RECIPIENT} from "../constants.js"
import * as Axios from "axios"

export default {
   data(){
      return {
         selected_email:       DEFAULT_RECIPIENT,
         clear_last_emailed:   true,
         set_subscribe_status: false,
         working:              false
      }
   },
   methods: {
      submit(){
         let data = {
               name: null,
               email: this.selected_email,
               clear_last_emailed: this.clear_last_emailed,
               has_unsubscribed: JSON.parse(this.set_subscribe_status )
            }
         console.log(data)
         this.working = true
         Axios.put(
            this.$public_url("/api/email-status"),
            JSON.stringify(data),
            {headers: {"Content-Type":"application/json"}})
            .then((r)=>{
               this.working = false
            })
            .catch((e)=>{
               this.working = false
            })
      }
   }
}
</script>
