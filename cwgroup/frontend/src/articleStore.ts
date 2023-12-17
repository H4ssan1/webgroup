import { defineStore } from 'pinia';

export const useArticleStore = defineStore('articleStore', {
  state: () => ({
    ids: [],
    titles: [],
    contents: [],
    categories: [],
  }),
  actions: {
    async fetchArticles() {
      try {
        const response = await fetch('http://127.0.0.1:8000/articles/');
        if (!response.ok) {
          throw new Error('Network response was not ok');
        }
        const articles = await response.json();

        this.ids = articles.map((article: { id: any; }) => article.id);
        this.titles = articles.map((article: { title: any; }) => article.title);
        this.contents = articles.map((article: { content: any; }) => article.content);
        this.categories = articles.map((article: { category__name: any; }) => article.category__name); // Adjust according to the actual field name
      } catch (error) {
        console.error('Error fetching articles:', error);
      }
    }
  }
});