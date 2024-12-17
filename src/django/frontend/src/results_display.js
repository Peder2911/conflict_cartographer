
import * as R from "ramda"
import union from "@turf/union"
import * as d3 from "d3"
import {round_to} from "@/util"

const GED_STYLE = {
   color: "#222",
   fillColor: "#d45",
   weight: 4,
   fillOpacity: 1,
}

const color_good_bad = d3.scaleLinear()
   .domain([0,1])
   .range(["#d45","#5a4"])

const props_of = (p) => R.map(R.prop(p))

function prediction_popup(props){
   return `
   <table>
      <tr>
         <td>Coverage</td>
         <td>${round_to(props.conflict_coverage,2)*100}%</td>
      </tr>
      <tr>
         <td>Predicted lower</td>
         <td>${props.casualties.lower}</td>
      </tr>
      <tr>
         <td>Predicted upper</td>
         <td>${props.casualties.upper}</td>
      </tr>
      <tr>
         <td>Actual casualties</td>
         <td>${round_to(props.actuals,2)}</td>
      </tr>
      <tr>
         <td>Added at</td>
         <td>${props.date}</td>
      </tr>
   </table>
   `
}

export const display_functions = {
   accuracy: {
      predictions: (feature_group)=>{
         feature_group.setStyle((feature)=>{
            return {
               color: feature.properties.correct == 1? "green":"red",
               fillOpacity: feature.properties.intensity != -1? 0.4:0.1,
               opacity: feature.properties.intensity != -1? 1:0.4,
            }
         })
         feature_group.eachLayer(lyr=>{
            lyr.bindPopup(prediction_popup(lyr.feature.properties))
         })
         return feature_group
      },

      points: (feature_group)=>{
         let features = []
         feature_group.eachLayer(lyr=>{
            features.push(lyr.feature)
         })

         feature_group = L.geoJSON(features,{
            pointToLayer: (ftr,latlng)=>{
               return L.circleMarker(latlng,{
                  radius: (Math.log(ftr.properties.best+1)+1)*5,
                  ...GED_STYLE
               })
            }
         })
         return feature_group 
      }, 

      buffered: null,
   },
   coverage: {
      predictions: (feature_group)=>{
         feature_group.setStyle(ftr=>{
            return {
               color: color_good_bad(ftr.properties.conflict_coverage),
               fillOpacity: 0.3
            }
         })
         return feature_group
      },

      points: (feature_group)=>{
         let features = props_of("feature")(feature_group.getLayers()) 
         feature_group = L.geoJSON(features,{
            pointToLayer: (_,latlng)=>{
               return L.circleMarker(latlng,{
                  ...GED_STYLE,
                  fillOpacity: 1,
                  fillColor: "#d45",
               })
            }
         })
         return feature_group
      }, 

      buffered: (feature_group)=>{
         let features = props_of("feature")(feature_group.getLayers())
         if(features.length>0){
            let buf_union = features.reduce((a,b)=>union(a,b))
            feature_group = L.geoJSON(buf_union)
            feature_group.setStyle({
               color: "#222",
               fillColor: "#d45",
               fillOpacity: 0.8,
            })
         }
         return feature_group
      },
   },
}


export function compute_stats(metric_name,data){
   let stats = {list:[], hero: 0}
   switch(metric_name){
      case "accuracy":
         stats.list.push({
            name: "Total casualties",
            value: R.compose(
               R.sum,
               props_of("best"),
               props_of("properties"),
               props_of("feature"),
            )(data.points.getLayers())
         })

         let correct_predictions = R.compose(
               R.sum,
               props_of("correct"),
               props_of("properties"),
               props_of("feature"), 
            )(data.predictions.getLayers())
         stats.list.push({
            name: "Correct predictions",
            value: correct_predictions,
         })

         let mean_accuracy = correct_predictions/data.predictions.getLayers().length

         stats.hero = `${mean_accuracy*100}%`
         break

      case "coverage":
         let mean_cov = R.compose(
            R.sum,
            props_of("conflict_coverage"),
            props_of("properties"),
            props_of("feature")
         )(data.predictions.getLayers())/data.predictions.getLayers().length
         stats.list.push({
            name: "Million km² predicted",
            value: R.compose(
               (x)=>round_to(x/1000000,2),
               R.sum,
               props_of("square_km_area"),
               props_of("properties"),
               R.filter(ftr=>ftr.properties.intensity!=-1),
               props_of("feature"),
            )(data.predictions.getLayers())
         })

         stats.hero = `${round_to(mean_cov*100,2)}%`
         break
   }
   return stats 
}
