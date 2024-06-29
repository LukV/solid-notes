<template>
  <div id="canvas">
    <aside :class="['sidebar', { open: isSidebarOpen }]">
      <SidebarHeader @toggle-sidebar="toggleSidebar" @add-note="addNote" />
      <SidebarContent />
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
            <select className="ql-header" defaultValue="3">
              <option value="1">Heading</option>
              <option value="2">Subheading</option>
              <option value="3">Normal</option>
            </select>
            <button class="ql-bold"></button>
            <button class="ql-italic"></button>
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
import SidebarHeader from '@/components/SidebarHeader.vue'
import SidebarContent from '@/components/SidebarContent.vue'
import { watch, onMounted, nextTick, ref } from 'vue'
import '@vueup/vue-quill/dist/vue-quill.bubble.css';
import '@vueup/vue-quill/dist/vue-quill.snow.css'

export default {
  name: 'App',
  components: {
    QuillEditor,
    SidebarHeader,
    SidebarContent
  },
  setup() {
    const noteStore = useNoteStore();

    onMounted(() => {
      noteStore.loadNotes();
      document.querySelector('.title-input').focus();

    });

    watch(() => noteStore.currentNote, () => {
      noteStore.saveNotes(); // Save notes whenever the current note is modified
    }, { deep: true });

    return {
      noteStore
    }
  },
  data() {
    return {
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

:root {
  color-scheme: only light;
}

body { 
   background-image: linear-gradient(#ffffff, #ffffff); 
   background-color: #ffffff;
}

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

strong {
  font-weight: bold !important;
}

strong em {
  font-weight: inherit !important;
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

.main-header {
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
    padding: 15px 0px;
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
  padding-left:15px;
}
</style>