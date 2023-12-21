// userStore.ts
import { defineStore } from 'pinia'

export const useUserStore = defineStore({
    id: 'user',
    state: () => ({
        username: '',
        email: '',
        dob: '',
        profilePic: '',
    }),
    actions: {
        fetchUserDetails() {
            fetch('http://127.0.0.1:8000/user_data/', {
                method: 'GET',
                headers: {
                    'Content-Type': 'application/json',
                    'Credentials': 'include',
                }
            })
                .then(response => response.json())
                .then(data => {
                    this.username = data.username;
                    this.email = data.email;
                    this.dob = data.date_of_birth;
                    this.profilePic = data.profile_image;
                })
                .catch(error => {
                    console.error('Error fetching user details:', error);
                });
        }
    }
});
