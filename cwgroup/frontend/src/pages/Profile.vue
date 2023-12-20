<template>
    <div>

        <div>profile image1</div>
        <img :src="userStore.profilePic" alt="Profile Picture" />
        <div>
            <h1>{{ userStore.username }}</h1>
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
            {{ email }}
            {{ dob }}

            <form @submit.prevent>
                <input type="email" v-model="email">
                <input type="date" v-model="dob">
                <button @click="updateUser">Update</button>
            </form>
        </div>
    </div>
</template>


<script lang="ts">
import { defineComponent, onMounted, ref } from "vue";
import { useUserStore } from "../userStore";

export default defineComponent({

    setup() {
        const userStore = useUserStore();

        onMounted(async () => {
            await userStore.fetchUserDetails();
            // You can handle any post-fetch logic here if needed
        });
        const email = ref(userStore.email);
        const dob = ref(userStore.dob);
        const updateUser = async () => {
            try {
                const response = await fetch('http://127.0.0.1:8000/update_user/', {
                    method: 'PUT',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({
                        email: email.value,
                        date_of_birth: dob.value,
                    })
                });

                if (!response.ok) {
                    throw new Error('Network response was not ok');
                }
            } catch (error) {
                console.error('There was an issue updating user:', error);
            }
        };


        return { userStore, email, dob, updateUser };
    }
})
</script>


