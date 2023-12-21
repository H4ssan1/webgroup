<template>
    <div>
        <button @click="Logout">Logout</button>
        <img :src="userStore.profilePic">
    </div>
    <div>{{ userStore.email }}</div>
    <div>{{ userStore.dob }}</div>
    <button @click="toggleEdit">Edit</button>
    <div v-if="editing">
        <form @submit.prevent>
            <input type="email" v-model="email">
            <input type="date" v-model="dob">
            <button @click="updateUser">Update</button>
        </form>
    </div>

    <div>
        <input type="file" @change="onFileChange" />
        <button @click="updateProfilePic">Upload</button>
    </div>

    <div>
        <h3>Select Favorite Categories</h3>
        <div v-for="category in allCategories" :key="category">
            <input type="checkbox" :value="category" :id="category" v-model="selectedCategories" />
            <label :for="category">{{ category }}</label>
        </div>
        <button @click="updateFavCategories">Update Categories</button>
    </div>
</template>
  
<script lang="ts">
import { defineComponent, ref, onMounted } from 'vue';
import { useUserStore } from '../userStore';

export default defineComponent({
    setup() {
        const userStore = useUserStore();
        const selectedFile = ref<File | null>(null);
        const editing = ref(false);
        const email = ref(userStore.email);
        const dob = ref(userStore.dob);
        const allCategories = ref(['Sports', 'World', 'Finance', 'Fashion', 'Health']);
        const selectedCategories = ref(userStore.favCategories);

        onMounted(async () => {
            await userStore.fetchUserDetails();
            email.value = userStore.email;
            dob.value = userStore.dob;
        });

        const toggleEdit = () => {
            editing.value = !editing.value;
        };
        const Logout = async () => {
            await fetch('http://127.0.0.1:8000/logout/',{});
            window.location.href = '/login/'; 
        };
        const updateUser = async () => {
            toggleEdit();
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
                    throw new Error('Error mate');
                }
            } catch (error) {
                console.error('There was an issue updating user:', error);
            }
            userStore.fetchUserDetails();
        };

        const onFileChange = (e: Event) => {
            const target = e.target as HTMLInputElement;
            if (target.files) {
                selectedFile.value = target.files[0];
            }
        };

        const updateProfilePic = async () => {
            if (selectedFile.value) {
                const formData = new FormData();
                formData.append('profile_pic', selectedFile.value);
                try {
                    const response = await fetch('http://127.0.0.1:8000/update_user_profilePic/', {
                        method: 'POST',
                        body: formData,
                    });
                    const data = await response.json();
                    console.log(data.message);
                } catch (error) {
                    console.error(error);
                }
            }
            userStore.fetchUserDetails();
        };

        const updateFavCategories = async () => {
            await userStore.updateFavCategories(selectedCategories.value);
        };

        return {
            userStore,
            email,
            dob,
            editing,
            toggleEdit,
            updateUser,
            selectedFile,
            onFileChange,
            updateProfilePic,
            allCategories,
            selectedCategories,
            updateFavCategories,
            Logout,
        };
    },
});
</script>
  

