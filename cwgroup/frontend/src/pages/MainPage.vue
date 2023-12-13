<template>
  <div>
    <h1>News</h1>

    <div v-for="article in articleStore.articles">
      <h2>{{ article.category }}</h2>


      {{ article.image }}
      <br>
      {{ article.text }}
      <br>
      {{ article.id }}
      <br>
      {{ article.category }}
    </div>
  </div>
</template>

<script lang="ts">
import { defineComponent } from "vue";
import { useArticleStore } from "../articleStore"

export default defineComponent({
  data() {
    return {
      title: "Main Page",
    }
  },
  setup() {
    const articleStore = useArticleStore();
    return { articleStore };
  }
})
</script>

<style scoped></style>
