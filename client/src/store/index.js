import { createStore } from 'vuex'
import auth from "@/store/modules/auth.js";
import documents from "@/store/modules/documents.js";


const store = createStore({
    modules: {
        auth,
        documents
    },
});

export default store;