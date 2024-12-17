<template>
   <div class="textwrapper">
      <div class="row"> 
         <div class="eight columns">
         <h1 class="title">Welcome!</h1>
            <p ><span >This is a brief tutorial that describes the purpose of the Conflict Cartographer, how to use it, and what we are planning to do with the data gathered from the Conflict Cartographer. You can re-open this tutorial at any time by pressing the question mark at the top of the page.</span></p>
            <p ><span ></span></p>
            <p ><span >Please read this tutorial before proceeding.</span></p>
            <h2  ><span >Purpose of the Conflict Cartographer</span></h2>
            <p ><span >The purpose of this tool is to collect and aggregate expert knowledge on the geographical distribution of conflict escalation and de-escalation.</span></p>
            <p ><span ></span></p>
            <p ><span >Your input will be used to investigate whether expert knowledge can help us improve sub-national early warning prediction models of violent conflict. </span></p>
            <p ><span ></span></p>
            <p ><span >Conflict escalation and de-escalation have proven to be difficult to predict. One cause for this could be that the relevant information is highly context sensitive and/or difficult to operationalize quantitatively. We hope that by leveraging the ability of humans to gather and assess a wide variety of information, we can improve our ability to predict year-by-year changes in conflict intensity at the sub-national level.</span></p>
            <h2  ><span >What we want you to do</span></h2>
            <p ><span >You have been assigned one or more country projects, where we would like you to draw the areas within (or close to the border) of the given country where you believe violent conflict will either escalate (either from nothing or from the conflict intensity this current year) or de-escalate next year.</span></p>
            <p ><span ></span></p>
            <p ><span>The data collected in this study are </span><span >shapes drawn on a map</span><span >. Each shape is associated with two variables.</span></p>
            <p ><span ></span></p>
            <p ><span>The first variable is your </span><span >predicted change in conflict intensity in the following year</span><span >, which is coded as one out of five values. These are -2 (&ldquo;Much less), -1 (&ldquo;Less&rdquo;), 0 (&ldquo;No change&rdquo;), 1 (&ldquo;More&rdquo;), 2 (&ldquo;Much more&rdquo;). Negative values mean a reduction in conflict intensity (de-escalation), while positive values mean an increase in conflict intensity (escalation).</span></p>
            <p ><span ></span></p>
            <p ><span >Areas can be left blank, which we take to mean that you believe that the intensity will stay the same.</span></p>
            <p ><span ></span></p>
            <p ><span>The second variable is </span><span >the confidence level you assign to the intensity coding</span><span >. This is a value between 0 and 1. It would be great if you use this scale to code your relative confidence across the areas you yourself code, rather than trying to match your own confidence to that of others. I.e. the areas you think you have relatively good information about should be coded with a relatively higher confidence than those you think you have relatively poor information about.</span></p>
            <p ><span ></span></p>
            <h2  ><span >Choosing a project</span></h2>
            <p ><span >Each project is represented by a card on the menu screen. Click a card to display the corresponding map, and to start adding area-layers.</span></p>
            <p ><span ></span></p>
            <p ><span >A project consists of a country and a project period for when it is possible to make changes to your predictions. Within the project period, you can come back and make changes. When the project period ends, we will lock the project for further changes. You will then not be able to open the project.</span></p>
            <h2  ><span >Using the map</span></h2>
            <p ><span>The areas are drawn on an interactive map. To draw on the map, you select the drawing tool from the top left on the screen, and click the map to place points. </span><span >Draw points until you have enclosed the area of interest, and then click the first point you placed to finish the area.</span></p>
            <p ><span ></span></p>
            <p ><span >Each area is associated with a box located to the right of the map, with two sliders. The sliders let you enter values for the two variables, associating them with the area that is highlighted. To delete a drawn area, press the orange button in the associated box.</span></p>
            <p ><span ></span></p>
            <p ><span >Your data is saved in real time. You can revisit and revise each country-project by going back and forth between the menu and the map. When you are done, simply close the browser window.</span></p>
            <h2  ><span >Who are we?</span></h2>
            <p ><span>We are conflict researchers based at the </span><span ><a  href="https://www.google.com/url?q=https://www.prio.org/&amp;sa=D&amp;ust=1574674058417000">Peace Research Institute Oslo</a></span><span>&nbsp;(PRIO). The Conflict Cartographer was made with funds from the </span><span ><a  href="https://www.google.com/url?q=https://www.eu-listco.net/&amp;sa=D&amp;ust=1574674058417000">EU-LISTCO</a></span><span >&nbsp;project, which is an EU Horizon 2020 project. To contact us about the Conflict Cartographer, please use the email:</span></p>
            <p ><span ></span></p>
            <p ><span ><a  href="mailto:conflictcartographer@prio.org">conflictcartographer@prio.org</a></span><span >&nbsp;</span></p>
            <p ><span ></span></p>
            <p ><span>You can also contact us individually. The project team consists of Jonas Vestby (</span><span ><a  href="mailto:jonves@prio.org">jonves@prio.org</a></span><span>), Siri Aas Rustad (</span><span ><a  href="mailto:sirir@prio.org">sirir@prio.org</a></span><span>), H&aring;vard Mokleiv Nyg&aring;rd (</span><span ><a  href="mailto:havnyg@prio.org">havnyg@prio.org</a></span><span>), Andreas F. Tollefsen (</span><span ><a  href="mailto:andreas@prio.org">andreas@prio.org</a></span><span>) and Peder Landsverk (</span><span ><a  href="mailto:pedlan@prio.org">pedlan@prio.org</a></span><span >).</span></p>
            <h2  ><span >What are we going to do with this data?</span></h2>
            <p ><span>Concretely, we are attempting to predict year-to-year changes in battle-related deaths as coded and collected by the </span><span ><a  href="https://www.google.com/url?q=https://ucdp.uu.se/&amp;sa=D&amp;ust=1574674058419000">Uppsala Conflict Data Program</a></span><span >&nbsp;(UCDP). The prediction models we will make are based on the UCDP Geocoded Event Dataset (GED). UCDP GED codes events that fits with the definition of a state-based event, a one-sided violence event, or a non-state violence event. We will use their estimate of the number of battle-related deaths for all these types of events as basis for our definition of conflict escalation and de-escalation.</span></p>
            <p ><span ></span></p>
            <p ><span >Each polygon you draw is saved in a PostgreSQL/PostGIS database with the following columns: coder_id, project_id, entry_date, intensity, confidence, geometry. The coder_id is a unique number of each participant. The project_id is a unique number for the country and coding period where data could be entered. entry_date is unique for each polygon, and is the last time you made coding changes to the polygon. Intensity and confidence are the variables we ask you to code, and geometry is the geospatial information needed to represent the polygon you have drawn.</span></p>
            <p ><span ></span></p>
            <p ><span >We will conduct several types of analyses of this data. The main analysis for this round of coding (December 2019) will be to test the predictions directly on the UCDP GED data for 2020, that is likely to be released in the middle of 2021. We hope to provide each participant with a report of how well they did vis-&agrave;-vis the data collected by the UCDP, as well as the overall results from this endeavor. </span></p>
             <p ><span ></span></p>
            <p ><span >In addition to this main analysis, we are interested in understanding the data we have collected better. We are for instance interested in how much data we get from the coders, how varied the coding entries are, and whether there is agreement or disagreement between coders. We will also experiment with geo-spatial models that interpolate and combine the predictions from individual coders to a single prediction.</span></p>
            <p ><span ></span></p>
            <p ><span >We aim to make the data publicly available</span><span >&nbsp;within a reasonable time after the coding period has ended and the coding decisions have been locked, contingent on an ethical evaluation of the release of the data. We will not disclose the list of participants, nor any connection between the coder_id and personally identifiable data such as email address. Making the data public early means that other research groups can make use of the data. We do not take any responsibility for the use of the released data by other parties.</span></p>
         </div>

         <div class="images four columns">
            <div class="imgwrapper">
               <img class="logoimage" :src="priologo" alt="">
            </div>
            <div class="imgwrapper">
               <img class="logoimage" :src="eulistcologo" alt="">
            </div>
         </div>
      </div>
      <div class="row">
         <h1 class="title">Thank you for your contribution!</h1>
      </div>
      <div class="row">
         <div class="eight columns">
            <span class="signature"><p>Håvard Nygaard</p></span>
            <span class="signature"><p>Siri A. Rustad</p></span>
            <span class="signature"><p>Jonas Vestby</p></span>
            <span class="signature"><p>Andreas Tollefsen</p></span>
            <span class="signature"><p>Peder Landsverk</p></span>
         </div>
         <div class="four columns">
            <div class="imgwrapper">
               <div class="row">
                  <img class="lowerlogo" :src="priologo" alt="">
               </div>
               <div class="row">
                  <img class="lowerlogo" :src="eulistcologo" alt="">
               </div>
            </div>
         </div>
      </div>
   </div>
</template>

<script>
import priologo from "../images/priologo.png"
import eulistcologo from "../images/eulistcologo.png"
import demogif from "../images/testdrive.gif"

export default {
   data(){
      return {
         priologo: priologo,
         eulistcologo: eulistcologo,
         demogif: demogif, 
      }
   }
}

</script>

<style lang="sass"> 
   @import "../sass/variables.sass"

   .signature
      color: gray 
      line-height: 0px
      font-size: 19px
      font-weight: lighter

   .title   
      color: $ui_highlight
      font-size: 55px 

   .note
      display: inline-block
      color: $ui_highlight

   .images
      padding-top: 100px
      padding-right: 40px

   .logoimage
      max-height: 100%
      max-width: 100%
      text-align: center

   .lowerlogo
      max-height: 50%
      max-width: 50%
      text-align: right 
      vertical-align: center

   #demogif
      max-width: 150%

   .imgwrapper
      padding: 10px 10px
      position: inline-block

   .row
      margin-right: 10px

</style>
