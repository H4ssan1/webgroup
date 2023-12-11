import { defineStore } from 'pinia';

export const useArticleStore = defineStore('articleStore', {
    state: () => ({
        articles: [
            { id: 1, text: "ipsem alsfjsklfsljfsl ejrlsjf dlkfslkjfsl fjsf", category: "world", image: "Image goes here" },
            { id: 2, text: "Chelse lost 2-1 to man utd", category: "sport", image: "Image goes here2" },
            { id: 3, text: "Dollar up agaisnt euro", category: "finance", image: "Image goes here3" },
        ]
    })

})