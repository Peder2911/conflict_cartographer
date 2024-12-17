<template>
   <div class="widget" v-if="value">🕊️</div>
</template>
<script>
import "@/sass/widget.sass"
export default {
   name: "NonanswerWidget",
   props: ["value"],
}
</script>
