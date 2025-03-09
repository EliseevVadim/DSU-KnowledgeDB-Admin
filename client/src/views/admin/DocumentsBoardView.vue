<script setup>
import { ref, onMounted, computed } from "vue";
import { useStore } from "vuex";
import { useRouter } from "vue-router";
import ConfirmDialog from '../../components/ConfirmDialog.vue'
import {tr} from "vuetify/locale";
import LoadingSpinner from "@/components/LoadingSpinner.vue";

const store = useStore();
const router = useRouter();

const limit = ref(10);
const page = ref(1);

const searchQuery = ref(null);

const showDocumentDetails = ref(false);
const showAddForm = ref(false);
const addFormValid = ref(false);
const confirmDialog = ref(null);

const loading = ref(false);

const file = ref(null);

const documents = computed(() => store.getters.DOCUMENTS);
const totalDocuments = computed(() => store.getters.TOTAL_DOCUMENTS);

const selectedDocument = ref({
    filename: 'default.txt',
    text: 'default'
});

const openDialog = (document) => {
    selectedDocument.value.filename = document.cmetadata.filename ?? document.cmetadata.source
    selectedDocument.value.text = document.document;
    showDocumentDetails.value = true;
};

const closeDialog = () => {
    showDocumentDetails.value = false;
};


const fetchDocuments = () => {
    const offset = (page.value - 1) * limit.value;
    store.dispatch("loadDocuments", { limit: limit.value, offset, query: searchQuery.value });
};

const deleteDocument = async (id, name) => {
    await confirmDialog.value.open('Подтверждение удаления файла',
        `Вы действительно хотите удалить файл: <b>${name}</b>?`)
        .then(() => {
            loading.value = true;
             store.dispatch('deleteDocument', id)
                .then(() => {
                    fetchDocuments();
                    loading.value = false;
                })
                .catch((error) => {
                    console.log(error);
                })
        })
        .catch(() => {

        })
};

const addDocument = () => {
    loading.value = true;
    store.dispatch('addDocument', file.value)
        .then(() => {
            fetchDocuments();
            closeAddForm();
            loading.value = false;
        })
        .catch((error) => {
            console.log(error);
        })
};

const closeAddForm = () => {
    showAddForm.value = false;
    file.value = null;
};

const searchDocuments = () => {
    page.value = 1;
    fetchDocuments();
};

const resetSearch = () => {
    searchQuery.value = ''
    fetchDocuments();
};

onMounted(fetchDocuments);
</script>

<template>
    <LoadingSpinner :loading="loading" />
    <v-container>
        <v-btn color="primary" class="mb-4" @click="showAddForm = true">
            <v-icon left>mdi-plus</v-icon> Добавить новый
        </v-btn>
        <v-text-field
            v-model="searchQuery"
            label="Поиск по названию файла"
            prepend-icon="mdi-magnify"
            clearable
            @click:prepend="searchDocuments"
            @keyup.enter="searchDocuments"
            @click:clear="resetSearch"
            class="mb-4"
        ></v-text-field>
        <v-table>
            <thead>
            <tr>
                <th>Название файла</th>
                <th>Текст</th>
                <th>Действия</th>
            </tr>
            </thead>
            <tbody>
            <tr v-for="doc in documents" :key="doc.id">
                <td>{{ doc.cmetadata.filename ?? doc.cmetadata.source }}</td>
                <td>{{ doc.document.slice(0, 100) }}...</td>
                <td>
                    <v-btn color="primary" icon @click="openDialog(doc)">
                        <v-icon>mdi-eye</v-icon>
                    </v-btn>
                    <v-btn color="red" icon @click="deleteDocument(doc.id, doc.cmetadata.filename ?? doc.cmetadata.source)">
                        <v-icon>mdi-delete</v-icon>
                    </v-btn>
                </td>
            </tr>
            </tbody>
        </v-table>
        <v-pagination
            v-model="page"
            :length="Math.ceil(totalDocuments / limit)"
            @update:model-value="fetchDocuments"
            class="mt-4"
        ></v-pagination>
        <v-dialog v-model="showDocumentDetails" max-width="600px">
            <v-card>
                <v-card-title>Документ</v-card-title>
                <v-card-text>
                    <p><strong>Название:
                    </strong> {{ selectedDocument.filename }}</p>
                    <br>
                    <p><strong>Содержимое:</strong> {{ selectedDocument.text }}</p>
                </v-card-text>
                <v-card-actions>
                    <v-btn color="primary" @click="closeDialog">Закрыть</v-btn>
                </v-card-actions>
            </v-card>
        </v-dialog>
        <v-dialog v-model="showAddForm" max-width="500px">
            <v-card>
                <v-card-title class="headline">Добавить документ</v-card-title>
                <v-card-text>
                    <v-form ref="addDocumentForm" v-model="addFormValid">
                        <v-file-input
                            v-model="file"
                            label="Выберите файл"
                            filled
                            dense
                            prepend-icon="mdi-paperclip"
                            accept=".pdf,.doc,.docx,.txt, .xlsx"
                            :rules="[v => !!v || 'Файл обязателен']"
                        ></v-file-input>
                    </v-form>
                    <v-overlay v-if="loading">
                        <v-progress-circular indeterminate size="50"></v-progress-circular>
                    </v-overlay>
                </v-card-text>
                <v-card-actions>
                    <v-spacer></v-spacer>
                    <v-btn color="blue darken-1" @click="closeAddForm">Отмена</v-btn>
                    <v-btn color="blue darken-1" @click="addDocument" :disabled="!addFormValid">Загрузить</v-btn>
                </v-card-actions>
            </v-card>
        </v-dialog>
        <ConfirmDialog ref="confirmDialog" />
    </v-container>
</template>


<style scoped>

</style>