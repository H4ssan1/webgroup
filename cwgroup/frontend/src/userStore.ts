import { defineStore } from 'pinia';

export const useUserStore = defineStore('userStore', {
    state: () => ({
        user: { id: 1, name: 'John', username: 'John123', email: 'john123@gmail.com', dob: '01/01/1990' },
    })

})
