
import * as d3 from "d3"

export let colorscale = d3.scaleLinear()
   .domain([1,5])
   .range(["blue","red"])

export let alphascale = d3.scaleLinear()
   .domain([0,100])
   .range([0.0,0.8])
