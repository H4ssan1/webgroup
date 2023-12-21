import { defineStore } from 'pinia';

interface Comment {
  id: number;
  content: string;
  user: string;
  created_at: string;
  parent_id: number | null;
  replies: Comment[];
}

export const useArticleStore = defineStore('articleStore', {
  state: () => ({
    ids: [] as number[],
    titles: [] as string[],
    contents: [] as string[],
    categories: [] as string[],
    comments: {} as Record<number, Comment[]>,
  }),
  actions: {
    async fetchArticles() {
      try {
        const response = await fetch('http://127.0.0.1:8000/articles/');
        if (!response.ok) {
          throw new Error('Error mate');
        }
        const articles = await response.json();
        this.ids = articles.map((article: { id: number }) => article.id);
        this.titles = articles.map((article: { title: string }) => article.title);
        this.contents = articles.map((article: { content: string }) => article.content);
        this.categories = articles.map((article: { category__name: string }) => article.category__name);
      } catch (error) {
        console.error('Error fetching articles', error);
      }
    },
    async fetchComments(articleId: number) {
      try {
        const response = await fetch(`http://127.0.0.1:8000/article/${articleId}/comments/`);
        if (!response.ok) {
          throw new Error('Error mate');
        }
        const comments = await response.json();
        this.comments[articleId] = this.formatComments(comments);
      } catch (error) {
        console.error('Error fetching comments:', error);
      }
    },
    formatComments(rawComments: any[]): Comment[] {
      const commentMap = new Map<number, Comment>();
      const rootComments: Comment[] = [];

      rawComments.forEach(commentData => {
        const comment: Comment = {
          ...commentData,
          replies: []
        };
        commentMap.set(comment.id, comment);
      });
      rawComments.forEach(commentData => {
        const comment = commentMap.get(commentData.id);
        if (comment && comment.parent_id) {
          const parent = commentMap.get(comment.parent_id);
          parent?.replies.push(comment);
        } else if (comment) {
          rootComments.push(comment);
        }
      });

      return rootComments;
    },

  }
});
