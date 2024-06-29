<template>
  <div id="canvas">
    <aside :class="['sidebar', { open: isSidebarOpen }]">
      <SidebarHeader @toggle-sidebar="toggleSidebar" @add-note="addNote" />
      <SidebarContent />
    </aside>
    <MainSection
      :isSidebarOpen="isSidebarOpen"
      :toggleSidebar="toggleSidebar"
      @add-note="addNote"
    />
  </div>
</template>

<script>
import { useNoteStore } from '@/stores/notesStore'
import SidebarHeader from '@/components/SidebarHeader.vue'
import SidebarContent from '@/components/SidebarContent.vue'
import MainSection from '@/components/MainSection.vue'
import { watch, onMounted } from 'vue'
import '@vueup/vue-quill/dist/vue-quill.bubble.css';
import '@vueup/vue-quill/dist/vue-quill.snow.css'

export default {
  name: 'App',
  components: {
    SidebarHeader,
    SidebarContent,
    MainSection
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
    background: linear-gradient(to bottom, #f5f5f5, #f5f5f5, #ece2e4); /* ece */
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

.ql-container.ql-snow {
  border: none;
}

.ql-toolbar.ql-snow {
  border: none;
  display: flex;
}
</style>
