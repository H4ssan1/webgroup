<template>
    <div>
        <img :src="userStore.profilePic">
    </div>
    {{ email }}
    {{ dob }}
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
</template>
  
<script lang="ts">
import { defineComponent, ref, onMounted } from 'vue';
import { useUserStore } from '../userStore';
export default defineComponent({

    setup() {
        const userStore = useUserStore();
        const selectedFile = ref<File | null>(null);
        const editing = ref(false);


        onMounted(async () => {
            await userStore.fetchUserDetails();
        });
        const email = ref(userStore.email);
        const dob = ref(userStore.dob);
        const toggleEdit = () => {
            editing.value = !editing.value;
        }

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
                    throw new Error('Network response was not ok');
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

        return {
            selectedFile,
            onFileChange,
            updateProfilePic,
            userStore,
            updateUser,
            email,
            dob,
            editing,
            toggleEdit,
        };
    },
});
</script>
  


