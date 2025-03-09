<script setup>
import { useStore } from 'vuex'
import { useRouter, useRoute } from 'vue-router'
import {computed, onMounted, ref} from 'vue'

const store = useStore()
const router = useRouter()
const route = useRoute()

const drawer = ref(false)

const isAuthenticated = computed(() => store.getters.isAuthenticated)

onMounted(() => {
    if (!isAuthenticated.value) {
        router.push('/login')
    }
})

const logout = async () => {
    store.dispatch('logout')
        .then(() => {
            router.push('/login')
        })
}
</script>

<template>
    <v-app>
        <v-navigation-drawer
            v-model="drawer"
            app
            color="primary"
            dark
            clipped
            floating
            temporary
        >
            <v-list dense>
                <v-list-item @click="router.push('/')">
                    <v-list-item-title>Главная</v-list-item-title>
                </v-list-item>
                <v-list-item @click="router.push('/documents')">
                    <v-list-item-icon>
                        <v-icon>mdi-file-document</v-icon>
                    </v-list-item-icon>
                    <v-list-item-title>Документы</v-list-item-title>
                </v-list-item>
                <v-spacer></v-spacer>
                <v-list-item @click="logout">
                    <v-list-item-icon>
                        <v-icon>mdi-logout</v-icon>
                    </v-list-item-icon>
                    <v-list-item-title>Выйти</v-list-item-title>
                </v-list-item>
            </v-list>
        </v-navigation-drawer>

        <v-app-bar app color="primary" dark>
            <v-app-bar-nav-icon @click="drawer = !drawer" />
            <v-toolbar-title>{{ route.meta.title }}</v-toolbar-title>

            <v-spacer></v-spacer>
            <v-btn @click="logout">Выйти</v-btn>
        </v-app-bar>

        <v-main>
            <v-container fluid>
                <router-view v-slot="{ Component }">
                    <component :is="Component" v-if="Component" />
                    <v-container v-else class="fill-height d-flex flex-column justify-center align-center text-center">
                        <v-icon size="80" color="primary">mdi-home</v-icon>
                        <h2 class="mt-3">Добро пожаловать!</h2>
                        <p class="text-medium-emphasis">
                            Выберите раздел в меню слева или начните с просмотра документов.
                        </p>
                        <v-btn color="primary" @click="router.push('/documents')" class="mt-3">
                            <v-icon left>mdi-file-document</v-icon> Перейти к документам
                        </v-btn>
                    </v-container>
                </router-view>
            </v-container>
        </v-main>
    </v-app>
</template>

<style scoped>

</style>