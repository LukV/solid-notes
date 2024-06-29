<template>
    <div class="sidebar-content">
        <h1>Solid Notes</h1>
        <nav>
            <ul>
                <li v-for="(note, index) in noteStore.notes" :key="index" class="note-item">
                    <a href="#" @click.prevent="setCurrentNote(index)">{{ note.title }}</a>
                    <span class="material-icons-outlined more-options"
                        @click.prevent="toggleContextMenu(index)">more_vert</span>
                    <div v-if="contextMenuVisible && currentContextIndex === index" class="context-menu">
                        <a href="#" @click.prevent="deleteNote(index)">Delete</a>
                    </div>
                </li>
            </ul>
        </nav>
    </div>
</template>

<script>
import { onMounted, ref } from 'vue'
import { useNoteStore } from '@/stores/notesStore'

export default {
    name: 'SidebarContent',
    props: {
        setCurrentNote: Function,
    },
    setup() {
        const contextMenuVisible = ref(false);
        const currentContextIndex = ref(null);
        const noteStore = useNoteStore();

        onMounted(() => {
            document.addEventListener('click', (event) => {
                if (!event.target.closest('.context-menu') && !event.target.closest('.more-options')) {
                    contextMenuVisible.value = false;
                    currentContextIndex.value = null;
                }
            });
        });

        return {
            contextMenuVisible,
            currentContextIndex,
            noteStore
        }
    },
    methods: {
        toggleContextMenu(index) {
            if (this.contextMenuVisible && this.currentContextIndex === index) {
                this.contextMenuVisible = false;
                this.currentContextIndex = null;
            } else {
                this.contextMenuVisible = true;
                this.currentContextIndex = index;
            }
        },
        deleteNote(index) {
            this.noteStore.deleteNote(index);
            this.contextMenuVisible = false;
        },
        setCurrentNote(index) {
            this.noteStore.setCurrentNote(index);
        },
    }
}
</script>

<style scoped>
/* Include the necessary styles here */
.sidebar-content {
    padding: 10px;
    overflow-y: auto;
    /* Ensure scrollbar applies only to the sidebar content */
    flex: 1;
    /* Ensure sidebar-content takes available space */
}

.sidebar-content h1 {
    margin: 10px;
}

.sidebar-content nav ul {
    list-style: none;
}

.note-item {
    position: relative;
    padding: 5px 25px 5px 10px;
    border-radius: 8px;
    transition: background-color 0.2s ease;
}

.note-item:hover {
    background-color: #e0e0e0;
}

.note-item .more-options {
    position: absolute;
    right: 10px;
    top: 50%;
    transform: translateY(-50%);
    cursor: pointer;
    display: none;
}

.note-item:hover .more-options {
    display: block;
}

.context-menu {
    position: absolute;
    right: 10px;
    top: 20px;
    background: white;
    border: 1px solid #ccc;
    box-shadow: 0px 2px 10px rgba(0, 0, 0, 0.1);
    border-radius: 5px;
    z-index: 1000;
}

.context-menu a {
    display: block;
    padding: 5px 10px;
    text-decoration: none;
    color: black;
}

.context-menu a:hover {
    background-color: #f0f0f0;
}
</style>