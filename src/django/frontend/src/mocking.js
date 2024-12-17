
function randomName(length){
   let letters = "abcdefghijklmnopqrstuvwxyz"
   if(length === undefined){
      length = 8
   }
   let current = ""
   for(let i = 0; i < length; i++){
      current = current + letters[Math.abs(Math.round(Math.random()*letters.length)-1)]
   }
   return current
}

export function mock_countries(n){
   // If given a number N, returns a list of N fake countries,
   // otherwise returns one mock country
   function mock_country(gwno){
      return {
         name: randomName(8),
         url: `http://www.foo.bar/${gwno}`,
         gwno: gwno,
         iso2c: "AF" 
      }
   }
   
   if(n !== undefined){
      let mocks = [] 
      for(let i = 0; i < n; i++){
         mocks.push(mock_country(i))
      }
      return mocks
   } else {
      return mock_country(432)
   }
}
