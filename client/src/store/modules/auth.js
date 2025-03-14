import axios from "axios";
import {config} from "@/config/config.js";
import store from "@/store/index.js";

const state = {
    access_token: localStorage.getItem('access_token') || null
};

const getters = {
    isAuthenticated: state => !!state.access_token
};

const mutations = {
    SET_ACCESS_TOKEN(state, token) {
        localStorage.setItem('access_token', token)
        state.access_token = token
    },
    REMOVE_ACCESS_TOKEN(state) {
        localStorage.removeItem('access_token')
        state.access_token = null
    }
};

const actions = {
    register: (context, payload) => {
        return new Promise(async (resolve, reject) => {
            await axios.post(config.apiUrl + '/auth/register', payload)
                .then((response) => {
                    resolve(response)
                })
                .catch((error) => {
                    reject(error)
                })
        })
    },
    login: (context, payload) => {
        return new Promise(async (resolve, reject) => {
            await axios.post(config.apiUrl + '/auth/login', payload)
                .then((response) => {
                    store.commit('SET_ACCESS_TOKEN', response.data.access_token)
                    resolve(response)
                })
                .catch((error) => {
                    reject(error)
                })
        })
    },
    logout: (context) => {
        return new Promise(async (resolve, reject) => {
            await axios.post(config.apiUrl + '/auth/logout')
                .then((response) => {
                    context.commit('REMOVE_ACCESS_TOKEN')
                    resolve(response)
                })
                .catch((error) => {
                    reject(error)
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