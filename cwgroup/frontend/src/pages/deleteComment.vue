<template>
    <form>
        <button @click="deleteComment">Confirm to delete</button>
    </form>
</template>


<script lang="ts">
import { defineComponent, ref } from "vue";


export default defineComponent({
    props: ['id'],

    setup(props) {


        const content = ref('')
        const deleteComment = async () => {
            try {
                const response = await fetch(`http://127.0.0.1:8000/comment/${props.id}/delete/`, {
                    method: 'DELETE',
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
        return { deleteComment }

    }
})
</script>