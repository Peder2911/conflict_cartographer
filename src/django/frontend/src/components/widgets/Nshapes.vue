<template>
   <div class="widget" v-if="value>0">✏️{{ value }}</div>
</template>
<style></style>
<script>
import "@/sass/widget.sass"
export default {
   name: "NshapesWidget",
   props: ["value"]
}
</script>
