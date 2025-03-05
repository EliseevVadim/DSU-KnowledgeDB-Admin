<script setup>
import { useStore } from 'vuex'
import { useRouter } from 'vue-router'
import {computed, onMounted} from 'vue'

const store = useStore()
const router = useRouter()

const isAuthenticated = computed(() => store.getters.isAuthenticated)

onMounted(() => {
    if (!isAuthenticated.value) {
        router.push('/login')
    }
})
</script>

<template>
    <v-app>
        <v-container>
            <v-btn color="primary">Vuetify is here</v-btn>
        </v-container>
    </v-app>
</template>

<style scoped>

</style>