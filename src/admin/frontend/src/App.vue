<template>
   <div id="root">
      <div class="panel">
         <h1 class="highlight-text">CC Admin</h1>
         <ul>
            <li>
               <router-link to="/">
                  <link-button>Home</link-button>
               </router-link>
            </li>
            <li>
               <router-link to="/email">
                  <link-button>Participation-based emailing</link-button>
               </router-link>
            </li>
            <li>
               <router-link to="/single-email">
                  <link-button>Single Email</link-button>
               </router-link>
            </li>
            <li>
               <router-link to="/email-status-management">
                  <link-button>Email Status Management</link-button>
               </router-link>
            </li>
            <li>
               <router-link to="/info">
                  <link-button>Info</link-button>
               </router-link>
            </li>
         </ul>
      </div>
      <router-view></router-view>
   </div>
</template>

<style>
html, body {
   padding: 0;
   margin: 0;
}
</style>

<style scoped lang="sass">
@import "/sass/variables.sass"
@import "/sass/style.sass"

#root
   height: 100%
   display: grid
   grid-template-columns: $sidebar-size auto
</style>

<script lang="js">
import SideBar from "/components/SideBar.vue"
import LinkButton from "/components/LinkButton.vue"
import Timeline from "/components/Timeline.vue"
export default {
   name: "app",
   components: {SideBar, LinkButton, Timeline},
}
</script>
