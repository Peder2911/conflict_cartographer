<template>
   <div id="pm-wrapper">
      <Waiver v-if="(!profile.waiver) && profileLoaded"/>
      <div id="pm" v-else>
         <div class="pane infobar" v-if="profileLoaded">
            <Profile :profile="profile"/>
            <Calendar/>
            <MainDescription/>
            <Feedback/>
            <Share/>
         </div>
         <Spinner v-else/>
         <div class="pane projects">
            <div id="projectlist" v-if="projectsLoaded">
               <div v-for="project in projects" class="pmcard" :key="project.url">
                  <ProjectView class="card"
                     :key="project.url"
                     :project="project"
                     v-on:chosen="chosen(project)"
                     v-on:deselected="refreshProjects">
                  </ProjectView>
               </div>
               <div class="pmcard">
                  <button class="alt to-assign" v-on:click="go_to_assign">Assign more countries</button>
               </div>
            </div>
            <Spinner v-else/>
         </div>
      </div>
   </div>
</template>

<style lang="sass" scoped>
@import "@/sass/variables.sass"

.to-assign
   height: 100px 
   width: 100%

div#pm-wrapper
   display: grid
   background: $ui_gray 

div#pm
   display: grid
   grid-template-columns: $menu-col-proportions 
   min-height: 0

div.pane
   margin: $menu-gaps 
   max-height: 100%
   min-height: 0px

div.infobar 
   min-height: 0
   max-height: 100%
   margin: $menu-gaps*6 0 0 $menu-gaps
   margin-top: $menu-gaps*6

.infobar > *
   margin-bottom: $menu-gaps

.pane.projects
   display: grid
   margin-bottom: 40px 

#projectlist
   background: $ui-background 
   border-radius: $roundedness
   overflow-y: scroll 

.pmcard
   margin: $menu-gaps $menu-gaps 0 $menu-gaps

h1#menuheader
   line-height: 20px 

</style>

<script charset="utf-8">
   import ProjectView from "./ProjectView.vue"
   import Spinner from "../components/Spinner"
   import Profile from "@/components/Profile"
   import Waiver from "@/components/Waiver"
   import MainDescription from "@/components/MainDescription"
   import Calendar from "@/components/Calendar"
   import Feedback from "@/components/Feedback"
   import Share from "@/components/Share"

   export default {
      name: "ProjectMenu",

      data(){
         return {
            projects: [],
            projectsLoaded: false,
            profileLoaded: false,
            profile: {waiver: true}
         }
      },

      components: {
         ProjectView,
         Spinner,
         Profile,
         MainDescription,
         Waiver,
         Calendar,
         Feedback,
         Share,
      },

      computed: {
         loaded(){
            return this.projectsLoaded && this.profileLoaded
         }
      },

      methods: {
         chosen: function(project){
            this.$router.push(`ctry/${project.gwno}`)
         },
         refreshProjects(){
            this.projectsLoaded = false
            this.$api.get.rel("assigned")
               .then((r)=>{
                  this.projects = r.data.countries
                  this.projects = this.projects.sort((a,b)=>{ 
                     if(a.name < b.name){return -1}
                     if(a.name > b.name){return 1}
                     return 0
                  })
                  this.projectsLoaded = true})
               .catch((e)=>{
                  console.error(e)
               })
         },
         go_to_assign(){
            this.$router.push("/assign")
         }
      },

      mounted(){
         this.refreshProjects()
         this.$api.get.rel("whoami")
            .then((r)=>{
               this.profile = r.data
               this.profileLoaded = true
            })
            .catch((e)=>{
               this.profile = {name: e}
            })
      }
   }
</script>
