<template>
    <div class="h1">
        {{ content }}
    </div>
    <form>
        <input type="text" v-model="content">
        <button @click="postComment">send</button>
    </form>
</template>

<script lang="ts">
import { defineComponent, ref } from "vue";
import { useArticleStore } from "../articleStore";
export default defineComponent({
    props: ['article'],
    setup(props) {
        const articleStore = useArticleStore();
        const content = ref("");

        const postComment = async () => {
            try {
                const response = await fetch(`http://127.0.0.1:8000/article/${props.article}/add_comment/`, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({ content: content.value })
                });

                if (!response.ok) {
                    throw new Error('Network response was not ok');
                }

                const result = await response.json();
                console.log(result.message);
                content.value = "";
            } catch (error) {
                console.error('There was an issue posting the comment:', error);
            }
        };

        return { articleStore, content, postComment };
    }

})

</script>

<style scoped></style>