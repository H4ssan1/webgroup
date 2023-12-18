<template>
  <div>
    <h1>News Articles</h1>
    <div v-if="loading">Loading articles...</div>
    <div v-else>
      <div v-for="(id, index) in articleStore.ids" :key="id">
        <h2>{{ articleStore.titles[index] }}</h2>
        <p>{{ articleStore.contents[index] }}</p>
        <p>Category: {{ articleStore.categories[index] }}</p>
        <h3>Comments:</h3>
        <div v-if="articleStore.comment_contents[id] && articleStore.comment_user[id]">
          <div v-for="(comment, index) in articleStore.comment_contents[id]" :key="index">
            <div>
              <p> {{ articleStore.comment_user[id][index] }}:{{ comment }}
              </p>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>


<script lang="ts">
import { defineComponent, ref, onMounted } from 'vue';
import { useArticleStore } from '../articleStore';

export default defineComponent({
  name: 'ArticleList',

  setup() {
    const articleStore = useArticleStore();
    const loading = ref(true);
    onMounted(async () => {
      await articleStore.fetchArticles();
      // Fetch comments for each article
      for (const articleId of articleStore.ids) {
        await articleStore.fetchComments(articleId);
      }
      loading.value = false;
    });
    //console.log(articleStore.comment_contents[]);
    return { articleStore, loading };
  }
});
</script>
