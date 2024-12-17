<template>
   <div class="modal-root">
      <div class="modal-card">
         <div class="header">
            <button v-on:click="$emit('closeme')" class="clickable modal-close-button">X</button>
         </div>
         <div class="inner-container">
            <slot>
            </slot>
         </div>
      </div>
   </div>
</template>

<style lang="sass">
@import "../sass/variables.sass"
@import "../sass/style.sass"

.modal-card
   background-color: #ddd
   padding: 5px 10px 40px 10px 
   display: grid
   grid-gap: 5px

$close-button-size: 15px

.modal-close-button
   //border-radius: $close-button-size*4
   width: $close-button-size * 2
   height: $close-button-size * 2 
   margin: 0
   padding: 0
   display: grid
   place-items: center
   font-size: 13px
   float: right
   border: none
   background-color: #fba
   font-weight: bold
   color: #832
</style>

<script>
export default {
   name: "modal"
}
</script>
