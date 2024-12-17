export let mean = (array)=>{
   if(array.length > 0){
      let sum = array.reduce((a,b)=>a+b)
      return sum / array.length
   } else {
      return 0 
   }
}
