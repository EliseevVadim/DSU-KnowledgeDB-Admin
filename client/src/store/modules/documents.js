import axios from "axios";
import {config} from "@/config/config.js";
import store from "@/store/index.js";

const state = {
    documents: [],
    total: 0
};

const getters = {
    DOCUMENTS: state => state.documents,
    TOTAL_DOCUMENTS: state => state.total
};

const mutations = {
    SET_DOCUMENTS(state, payload) {
        state.documents = payload.documents
        state.total = payload.total
    }
};

const actions = {
    loadDocuments: async (context, { limit, offset }) => {
        await axios.get(config.apiUrl + '/documents', {
            params: { limit, offset },
            headers: config.headers
        })
            .then((response) => {
                context.commit('SET_DOCUMENTS', response.data)
            })
    },
    addDocument: (context, payload) => {
        return new Promise(async (resolve, reject) => {
            let formData = new FormData()
            formData.append('file', payload)
            await axios.post(config.apiUrl + '/documents/upload', formData, {
                headers: config.headers
            })
                .then((response) => {
                    resolve(response);
                })
                .catch((error) => {
                    reject(error);
                })
        })
    },
    deleteDocument: (context, id) => {
        return new Promise(async (resolve, reject) => {
            await axios.delete(config.apiUrl + '/documents/' + id, {
                headers: config.headers
            })
                .then((response) => {
                    resolve(response);
                })
                .catch((error) => {
                    reject(error);
                })
        })
    }
};

export default {
    state,
    getters,
    mutations,
    actions,
};