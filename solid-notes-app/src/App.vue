<template>
  <div id="canvas">
    <aside :class="['sidebar', { open: isSidebarOpen }]">
      <div class="sidebar-header">
        <button @click="toggleSidebar" class="toggle-sidebar-button">
          <span class="material-icons-outlined">view_sidebar</span>
        </button>
        <button @click="addNote" class="new-note-button">
          <span class="material-icons-outlined">edit</span>
        </button>
      </div>
      <div class="sidebar-content">
        <h1>Solid Notes</h1>
        <nav>
          <ul>
            <li v-for="(note, index) in noteStore.notes" :key="index" class="note-item">
              <a href="#" @click.prevent="setCurrentNote(index)">{{ note.title }}</a>
              <span class="material-icons-outlined more-options" @click.prevent="toggleContextMenu(index)">more_vert</span>
              <div v-if="contextMenuVisible && currentContextIndex === index" class="context-menu">
                <a href="#" @click.prevent="deleteNote(index)">Delete</a>
              </div>
            </li>
          </ul>
        </nav>
      </div>
    </aside>
    <main class="main-section" :class="{ expanded: !isSidebarOpen }">
      <header class="main-header">
        <span>
          <div v-if="!isSidebarOpen" class="top-buttons">
            <button @click="toggleSidebar" class="toggle-sidebar-button">
              <span class="material-icons-outlined">view_sidebar</span>
            </button>
            <button @click="addNote" class="new-note-button">
              <span class="material-icons-outlined">edit</span>
            </button>
          </div>
          {{noteStore.currentNote.title}}
        </span>
        <span id="toolbar-container">
          <span class="ql-formats">
            <button class="ql-bold"></button>
            <button class="ql-italic"></button>
            <button class="ql-underline"></button>
            <button class="ql-list" value="ordered"></button>
            <button class="ql-list" value="bullet"></button>
            <button class="ql-link"></button>
            <button class="ql-image"></button>
            <button class="ql-code-block"></button>
          </span>
        </span>
        <span>...</span>
      </header>
      <div class="title-block">
        <div class="content-block">
          <input 
              v-model="noteStore.currentNote.title" 
              placeholder="Title" 
              class="title-input"
              @blur="checkAndSubmitNote"
              @submit="checkAndSubmitNote"
            />
            <button v-if="isNewNote" @click="checkAndSubmitNote" class="submit-note-button">
              <span class="material-icons-outlined">check</span>
            </button>
        </div>  
      </div>
      <div class="main-content">
        <div class="content-block">
          <quill-editor 
            ref="quillEditor"
            v-model:content="noteStore.currentNote.content" 
            contentType="html" 
            :options="editorOptions" 
          />
        </div>
      </div>
    </main>
  </div>
</template>

<script>
import { QuillEditor } from '@vueup/vue-quill'
import { useNoteStore } from '@/stores/notesStore'
import { watch, onMounted, nextTick, ref } from 'vue'
import '@vueup/vue-quill/dist/vue-quill.bubble.css';
import '@vueup/vue-quill/dist/vue-quill.snow.css'

export default {
  name: 'App',
  components: {
    QuillEditor
  },
  setup() {
    const noteStore = useNoteStore();
    const contextMenuVisible = ref(false);
    const currentContextIndex = ref(null);

    onMounted(() => {
      noteStore.loadNotes();
      document.querySelector('.title-input').focus();
      
      document.addEventListener('click', (event) => {
        if (!event.target.closest('.context-menu') && !event.target.closest('.more-options')) {
          contextMenuVisible.value = false;
          currentContextIndex.value = null;
        }
      });
    });

    watch(() => noteStore.currentNote, () => {
      noteStore.saveNotes(); // Save notes whenever the current note is modified
    }, { deep: true });

    return {
      noteStore,
      contextMenuVisible,
      currentContextIndex
    }
  },
  data() {
    return {
      isNewNote: sessionStorage.getItem('isNewNote') === 'true',
      isSidebarOpen: true,
      editorOptions: {
        modules: {
          toolbar: '#toolbar-container'
        },
        theme: 'snow',
      }
    }
  },
  methods: {
    toggleSidebar() {
      this.isSidebarOpen = !this.isSidebarOpen;
    },
    addNote() {
      this.noteStore.addNote();
      document.querySelector('.title-input').focus();
    },
    deleteNote(index) {
      this.noteStore.deleteNote(index);
      this.contextMenuVisible = false;
    },
    setCurrentNote(index) {
      this.noteStore.setCurrentNote(index);
    },
    toggleContextMenu(index) {
      if (this.contextMenuVisible && this.currentContextIndex === index) {
        this.contextMenuVisible = false;
        this.currentContextIndex = null;
      } else {
        this.contextMenuVisible = true;
        this.currentContextIndex = index;
      }
    },
    checkAndSubmitNote() {
      if (sessionStorage.getItem('isNewNote') === 'true' && this.noteStore.currentNote.title.trim()) {
        this.noteStore.submitNote();
      }
    }
  }
}
</script>



<style>
@import url('https://fonts.googleapis.com/icon?family=Material+Icons+Outlined');

* {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
    line-height: 1.4;
    font-size: 14px;
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif, "Apple Color Emoji", "Segoe UI Emoji", "Segoe UI Symbol";
}

body, html {
    height: 100%;
}

#canvas {
    display: flex;
    height: 100vh;
    overflow: hidden; /* Prevent body from scrolling */
}

.sidebar, .main-section {
    display: flex;
    flex-direction: column;
    height: 100%;
}

.sidebar {
    width: 300px;
    overflow-y: auto;
    background: linear-gradient(to bottom, #f5f5f5, #f5f5f5, #ece2e4);
    transition: transform 0.3s ease;
    transform: translateX(0);
    position: absolute;
    left: 0;
}

.sidebar.open {
    transform: translateX(0);
}

.sidebar:not(.open) {
    transform: translateX(-100%);
}

.sidebar h1 {
    font-size: 24px;
    margin-bottom: 20px;
}

.sidebar nav ul li a {
    text-decoration: none;
    color: #333;
}

.main-section {
    flex: 1;
    overflow-y: auto;
    transition: width 0.3s ease, margin-left 0.3s ease;
    width: calc(100% - 300px); /* Adjust width when sidebar is open */
    margin-left: 300px; /* Adjust margin when sidebar is open */
}

.main-section.expanded {
    margin-left: 0;
    width: 100%; /* Expand to full width when sidebar is closed */
}

.sidebar-header, .main-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    height: 60px;
    padding: 0 15px;
    position: sticky;
    top: 0;
    z-index: 1;
    border-bottom: 1px solid #efefef;
}

.toggle-sidebar-button,
.new-note-button {
    background: none;
    border: none;
    cursor: pointer;
    color: #666;
    transition: color 0.3s ease;
}

.toggle-sidebar-button:hover,
.new-note-button:hover {
    color: #007bff;
}

.sidebar-header button:last-child {
    margin-right: 0;
}

.sidebar-content {
    padding: 10px;
    overflow-y: auto; /* Ensure scrollbar applies only to the sidebar content */
    flex: 1; /* Ensure sidebar-content takes available space */
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

.main-header .top-buttons {
    display: inline-flex;
    align-items: center;
}

.top-buttons > button {
    margin-right: 10px;
    margin-top: 2px;
}

.main-header > span:first-child {
    display: flex;
    align-items: center;
}

.main-content {
    display: flex;
    justify-content: center;
    overflow-y: auto; /* Ensure scrollbar applies only to the main content */
    flex: 1; /* Ensure main-content takes available space */
}

.title-block {
    display: flex;
    justify-content: center;
    padding: 15px 20px;
    border-bottom: 1px solid #efefef;
}

.content-block {
    width: 100%;
    max-width: 1024px;
    background-color: #fff;
}

.ql-container.ql-snow {
  border: none;
}

.ql-toolbar.ql-snow {
  border: none;
  display: flex;
}

#toolbar-container {
  /* Add your custom styles here */
  margin: 0px 10px;
}

/* Styles for the title input */
.title-input {
  font-size: 24px; /* Large font size */
  border: none; /* Remove border */
  outline: none; /* Remove outline */
  width: 100%; /* Full width */
  margin-left: 15px;
}
</style>