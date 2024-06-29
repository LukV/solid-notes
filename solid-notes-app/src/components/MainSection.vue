<template>
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
  </template>
  
  <script>
  import { QuillEditor } from '@vueup/vue-quill'
  import { useNoteStore } from '@/stores/notesStore'
  import { ref } from 'vue'
  
  export default {
    name: 'MainSection',
    components: {
      QuillEditor
    },
    props: {
      isSidebarOpen: Boolean,
      toggleSidebar: Function,
      addNote: Function
    },
    setup() {
      const noteStore = useNoteStore();
  
      return {
        noteStore,
        editorOptions: {
          modules: {
            toolbar: '#toolbar-container'
          },
          theme: 'snow',
        }
      }
    },
    methods: {
        checkAndSubmitNote() {
            if (sessionStorage.getItem('isNewNote') === 'true' && this.noteStore.currentNote.title.trim()) {
                this.noteStore.submitNote();
            }
        }
    }
  }
  </script>
  
  <style scoped>
  /* Include only the styles relevant to MainSection */
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
  