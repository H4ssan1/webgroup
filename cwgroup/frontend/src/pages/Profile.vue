<template>
    <div>

        <div>profile image</div>
        <div>
            <h1>{{ userStore.user.name }}</h1>
        </div>
        <div>
            favourite News categories:
            <br>
            <input type="checkbox" id="sport" name="sport" value="sport">
            <label for="sport">sport</label><br>
            <input type="checkbox" id="finance" name="finance" value="finance">
            <label for="finance">finance</label><br>
            <input type="checkbox" id="World" name="World" value="World">
            <label for="World">World</label><br>
        </div>



    </div>
</template>


<script lang="ts">
import { defineComponent, } from "vue";
import { useUserStore } from "../userStore";

export default defineComponent({
    data() {
        return {
            title: "Profile Page",
        };
    },
    setup() {
        const userStore = useUserStore();
        return { userStore };
    }
})
</script>


