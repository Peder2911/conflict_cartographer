<template>
   <div>
      <h2>{{question.label}}</h2>
      <p>{{question.description}}</p>
      <input v-model="question.value" type="text">
   </div>
</template>
<style></style>
<script>
export default {
   props: ["question"]
}
</script>
