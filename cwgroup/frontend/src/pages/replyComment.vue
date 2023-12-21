<template>
    <div>{{ content }}</div>
    <form>
        <input type="text" v-model="content">
        <button @click="replyComment">Send reply</button>
    </form>
</template>

<script lang="ts">
import { defineComponent, ref } from 'vue';

export default defineComponent({
    props: ['parent', 'article'],
    setup(props) {

        const content = ref('');
        const replyComment = async () => {
            try {
                const response = await fetch(`http://127.0.0.1:8000/article/${props.article}/add_comment/`, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({
                        content: content.value,
                        parent_id: props.parent

                    })
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

        return { content, replyComment }

    }
})
</script>