import { defineStore } from 'pinia';

export const useArticleStore = defineStore('articleStore', {
  state: () => ({
    ids: [],
    titles: [],
    contents: [],
    categories: [],
    comment_ids: {} as Record<number, Comment[]>,
    comment_contents: {} as Record<number, Comment[]>,
    comment_user: {} as Record<number, Comment[]>,
    //comments: {} as Record<number, Comment[]>,
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
    },
    async fetchComments(articleId: number) {
      try {
        const response = await fetch(`http://127.0.0.1:8000/article/${articleId}/comments/`);
        if (!response.ok) {
          throw new Error('Network response was not ok');
        }
        const comments = await response.json();
        this.comment_ids[articleId]= comments.map((comment: { id: any; }) => comment.id);
        this.comment_contents[articleId] = comments.map((comment: { content: any; }) => comment.content);
        this.comment_user[articleId] = comments.map((comment: { user: any; }) => comment.user);
        
        //this.comments[articleId] = comments; // Store the comments in the state
      } catch (error) {
        console.error('Error fetching comments:', error);
      }
    }
  }
});