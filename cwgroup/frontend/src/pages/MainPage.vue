<template>
  <div>
    <h1>News Articles</h1>
    <div v-if="loading">Loading articles...</div>
    <div v-else>
      <div v-for="(id, index) in articleStore.ids" :key="id">
        <div v-if="userStore.favCategories.includes(articleStore.categories[index])">
          <h2>{{ articleStore.titles[index] }}</h2>
          <p>{{ articleStore.contents[index] }}</p>
          <p>Category: {{ articleStore.categories[index] }}</p>
          <h3>Comments:</h3>
          <div v-if="articleStore.comments[id]">
            <div v-for="comment in articleStore.comments[id]" :key="comment.id">
              <p>{{ comment.user }}: {{ comment.content }}</p>
              <div v-if="userStore.username == comment.user">
                <button @click="toggleEdit(comment.id)">Edit</button>
                <button @click="toggleDelete(comment.id)">Delete</button>
                <div v-if="editingComment && editingID === comment.id">
                  <editComment :content="comment.content" :id="comment.id" />
                </div>
                <div v-if="deleteComment && deleteID === comment.id">
                  <deleteComment :id="comment.id" />
                </div>
              </div>
              <div v-if="comment.replies" class="replies">
                <div v-for="reply in comment.replies" :key="reply.id">
                  <p>{{ reply.user }}: {{ reply.content }}</p>
                  <div v-if="userStore.username == reply.user">
                    <button @click="toggleEdit(reply.id)">Edit Reply</button>
                    <button @click="toggleDelete(reply.id)">Delete</button>
                    <div v-if="editingComment && editingID === reply.id">
                      <editComment :content="reply.content" :id="reply.id" />
                    </div>
                    <div v-if="deleteComment && deleteID === reply.id">
                      <deleteComment :id="reply.id" />
                    </div>
                  </div>
                </div>
              </div>
              <button @click="toggleReply(comment.id)">Reply</button>
              <div v-if="replyingComment && comment.id === replyID">
                <replyComment :parent="comment.id" :article="id" />
              </div>
            </div>
          </div>
          <button @click="toggleAdd(id)"> Add a comment</button>
          <div v-if="addingComment && id === addingCommentID">
            <createComment :article=id />
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script lang="ts">
import { defineComponent, ref, onMounted } from 'vue';
import { useArticleStore } from '../articleStore';
import { useUserStore } from '../userStore';
import createComment from './createComment.vue'
import replyComment from './replyComment.vue'
import editComment from './editComment.vue';
import deleteComment from './deleteComment.vue'

export default defineComponent({

  components: { createComment, replyComment, editComment, deleteComment },
  setup() {
    const userStore = useUserStore();
    onMounted(async () => {
      await userStore.fetchUserDetails();
    });
    console.log(userStore.username);



    const articleStore = useArticleStore();
    const loading = ref(true);
    const addingComment = ref(false);
    const addingCommentID = ref<number>();
    const replyingComment = ref(false);
    const replyID = ref<number>();
    const editingID = ref<number>();
    const editingComment = ref(false);
    const deleteComment = ref(false);
    const deleteID = ref<number>();

    const toggleAdd = (id: number) => {
      addingCommentID.value = id;
      addingComment.value = !addingComment.value;
    }
    const toggleReply = (id: number) => {
      replyID.value = id;
      console.log(replyID);
      replyingComment.value = !replyingComment.value;
    }

    const toggleEdit = (id: number) => {
      editingID.value = id;
      editingComment.value = !editingComment.value;

    }
    const toggleDelete = (id: number) => {
      deleteID.value = id;
      deleteComment.value = !deleteComment.value;

    }

    onMounted(async () => {
      await articleStore.fetchArticles();
      for (const articleId of articleStore.ids) {
        await articleStore.fetchComments(articleId);
      }
      loading.value = false;
    });



    return { articleStore, loading, addingComment, toggleAdd, toggleReply, replyingComment, replyID, addingCommentID, userStore, toggleEdit, editingComment, editingID, toggleDelete, deleteID, deleteComment };

  },

});
</script>

<style scoped>
.replies {
  margin-left: 25px;
  border-left: 4px solid #2d08e4;
  padding-left: 15px;
}
</style>
