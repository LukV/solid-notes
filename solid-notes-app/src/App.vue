<template>
  <div id="canvas">
    <div :class="['sidebar', { open: isSidebarOpen }]">
      <h1>Solid Notes</h1>
      <nav>
        <ul>
          <li v-for="(note, index) in noteStore.notes" :key="index"><a href="#">{{ note.title }}</a></li>
        </ul>
      </nav>
    </div>
    <div class="main">
      <Editor />
    </div>
  </div>
</template>

<script>
import Editor from './components/Editor.vue'
import { useNoteStore } from '@/stores/notesStore'
import { ref, onMounted } from 'vue'

export default {
  name: 'App',
  components: {
    Editor
  },
  setup() {
    const noteStore = useNoteStore();

    onMounted(() => {
      noteStore.loadNotes();
    });

    return {
      noteStore
    }
  },
  data() {
    return {
      isSidebarOpen: true,
      notes: [
        { id: 1, title: 'Note 1' },
        { id: 2, title: 'Note 2' },
        // Add more notes here
      ]
    }
  },
  methods: {
    toggleSidebar() {
      this.isSidebarOpen = !this.isSidebarOpen;
    }
  }
}
</script>

<style>
#canvas {
  display: flex;
  height: 100vh;
}

.sidebar {
  width: 250px;
  background-color: #f4f4f4;
  padding: 20px;
  transition: transform 0.3s ease;
}

.sidebar.open {
  transform: translateX(0);
}

.sidebar h1 {
  font-size: 24px;
  margin-bottom: 20px;
}

.sidebar nav ul {
  list-style-type: none;
  padding: 0;
}

.sidebar nav ul li {
  margin-bottom: 10px;
}

.sidebar nav ul li a {
  text-decoration: none;
  color: #333;
}

.main {
  flex-grow: 1;
  display: flex;
  flex-direction: column;
}

.quill-editor {
  flex-grow: 1;
  display: flex;
  flex-direction: column;
}
</style>
