import * as L from "leaflet"

export function ged_point(_,latlng){
   return L.circleMarker(latlng,{
      radius: 8,
      fillColor: "#d45",
      color: "#222",
      weight: 4,
      fillOpacity: 1,
   })
}
