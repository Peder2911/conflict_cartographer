
<template>
   <div :id="id">
   </div>
</template>

<script>
import * as d3 from "d3"

export default {
   name: "timeline",
   props: {
      plotwidth: {
         type: Number,
         default: 300
      },
      plotheight: {
         type: Number,
         default: 200
      },
      margins:  {
         type: Number,
         default: 32 
      },
      features: {
         type: Array,
         default: []
      }
   },

   computed: {
      id(){
         return `_${this._uid}`
      }
   },

   data(){
      return {
         x: d3.scaleTime()
            .range([0+this.margins, this.plotwidth-(this.margins*.8)])
            .nice(),

         y: d3.scaleLinear() 
         .range([0+this.margins, this.plotheight - this.margins])
      }
   },

   mounted() {
      this.svg = d3.select(`#${this.id}`)
         .append("svg:svg")
         .attr("width", `${this.plotwidth}px`)
         .attr("height", `${this.plotheight}px`)
         .attr("fill", "#f00")

      this.xaxis = this.svg.append("svg:g")
         .attr("transform", `translate(0,${this.plotheight - this.margins})`)
         .call(d3.axisBottom(this.x))

      this.yaxis = this.svg.append("svg:g")
         .attr("transform", `translate(${this.margins},0)`)
         .call(d3.axisLeft(this.y))
   },
   watch: {
      features(features){
         let data = d3.nest()
            .key((ft)=>new Date(ft.year, (ft.quarter*3)-1, 0,0,0,0))
            .rollup((s)=> d3.mean(d => d[this.yfeature]))
            .entries(features)
         /* ... */
      }
   }
}
</script>
