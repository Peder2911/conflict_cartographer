<template>
   <div id="root">
      <div v-if="!accepted" id="modal">
         <div id="consentcard">
            <h1>Hey!</h1>
            <p id="infotext">
               By continuing to use this page, you consent to the storage of
               your contact information in our database. <br> Your information will
               be treated confidentially. 
            </p>
            <button v-on:click="accept">That's ok!</button>
         </div>
      </div>
   </div>
</template>

<style scoped>
body {
   padding: 0;
   margin: 0;
}

button {
   margin: 20px;
   font-size: 20px;
   width: 180px;
   height: 80px;
}

button:hover{
   background-color: white;
   cursor: pointer;
}

#modal {
   position: absolute;
   display: grid;
   place-items: center;
   top: 0;
   left: 0;
   height: 100vh;
   width: 100vw;
   background: rgba(200,200,200,0.8);
}
#consentcard {
   display: grid;
   place-items: center;
   grid-gap: 10px;
   text-align: center;
   background: #f0f0f0;
   border-radius: 12px;
   font-size: 20px;
   padding: 80px;
}
</style>
<script>
export default {
   name: "ConsentModal",
   data(){
      return {
         accepted: false
      }
   },
   mounted(){
      let consent = this.$cookies.get("consent")
      if(consent){
         this.accepted = true
      }
   },
   methods: {
      accept(){
         this.$cookies.set("consent",true)
         this.accepted = true
      }
   }
}
</script>
