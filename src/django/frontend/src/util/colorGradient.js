
const hexToRgb = function(hex){
   const lrepr = hex.split("")
   return [1,2,3].map(function(i){
      let left = (i * 2) - 1
      let right = left + 2
      let tuple = lrepr.slice(left,right).join("")
      return parseInt(tuple, 16)
   })
}

const ceil = (x) => x > 255 ? 254 : x;

const pad = function(x,digits){
   return "0".repeat(digits - x.length) + x;
}

const rgbToHex = function(r,g,b){
   let rgb = [r,g,b].map(ceil)
   let hexvalues = rgb.map(function(v){
      return Number(Math.round(v)).toString(16)
   })
   hexvalues = hexvalues.map(function(hv){
      return pad(hv,2)
   })

   return "#" + hexvalues.join("")
}

const rgbDiff = function(delta, x, y){
   let diff = y.map(function(e,i){
      return e - x[i]
   })
   return y.map(function(e,i){
      return Math.round((diff[i] * delta) + x[i])
   })
}

export default function colorGradient(delta, x, y){
   const result = rgbDiff(delta, hexToRgb(x), hexToRgb(y))
   return rgbToHex(...result);
}
