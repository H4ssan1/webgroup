// userStore.ts
import { defineStore } from 'pinia'

export const useUserStore = defineStore({
    id: 'user',
    state: () => ({
        username: '',
        email: '',
        dob: '',
        profilePic: '',
        favCategories: [] as string[],
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
                    this.favCategories = data.fav_categories;
                })
                .catch(error => {
                    console.error('Error fetching user details:', error);
                });
        },
        updateFavCategories(categories: string[]) {
            fetch('http://127.0.0.1:8000/update_fav_categories/', {
                method: 'PUT',
                headers: {
                    'Content-Type': 'application/json',
                    'Credentials': 'include',
                },
                body: JSON.stringify({ fav_categories: categories }),
            })
                .then(response => {
                    if (!response.ok) {
                        throw new Error('Failed to update fav categories');
                    }
                    return response.json();
                })
                .then(data => {
                    this.favCategories = categories;
                    console.log(data.message);
                })
                .catch(error => {
                    console.error('Error updating favorites', error);
                });
        },
    }
});
