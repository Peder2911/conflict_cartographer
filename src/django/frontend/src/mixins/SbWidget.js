export default {
   data(){
      return {
         active: false,
         mode: "inactive",
         msg: ""
      }
   },
   methods: {
      toggle(){
         if(!this.active){
            this.mode = "active"
            this.active = true
            this.msg = ""
         } else {
            this.mode = "thanks"
            setTimeout(()=>{
               this.mode = "inactive"
               this.active = false
            },1200)
         }
      },
   }
}
