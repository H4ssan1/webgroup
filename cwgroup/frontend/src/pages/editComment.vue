<template>
    <form>
        <input type="text" v-model="con">
        <button @click="editComment">Edit</button>
    </form>
</template>


<script lang="ts">
import { defineComponent, ref } from "vue";


export default defineComponent({
    props: ['id', 'content'],

    setup(props) {


        const con = ref(props.content)
        const editComment = async () => {
            try {
                const response = await fetch(`http://127.0.0.1:8000/comment/${props.id}/edit/`, {
                    method: 'PUT',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({
                        content: con.value,

                    })
                });

                if (!response.ok) {
                    throw new Error('Network response was not ok');
                }

                const result = await response.json();
                console.log(result.message);
                // Handle success - maybe clear the comment field or update UI
                con.value = "";  // Clear the input field after posting
            } catch (error) {
                console.error('There was an issue posting the comment:', error);
            }
        };
        return { con, editComment }

    }
})
</script>