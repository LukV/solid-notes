<template>
  <div id="canvas">
    <div :class="['sidebar', { open: isSidebarOpen }]">
      <div class="navbar">
        <button @click="toggleSidebar" class="toggle-sidebar-button">
          <span class="material-icons-outlined">view_sidebar</span>
        </button>
        <button @click="addNote" class="new-note-button">
          <span class="material-icons-outlined">edit</span>
        </button>
      </div>
      <h1>Solid Notes</h1>
      <hr class="divider">
      <nav>
        <ul>
          <li v-for="(note, index) in noteStore.notes" :key="index">
            <a href="#" @click.prevent="setCurrentNote(index)">{{ note.title }}</a>
            <a href="#" @click.prevent="deleteNote(index)">[x]</a>
          </li>
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
import { onMounted } from 'vue'

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

    const addNote = () => {
      noteStore.addNote();
    }

    const deleteNote = (index) => {
      noteStore.deleteNote(index);
    }

    const setCurrentNote = (index) => {
      noteStore.setCurrentNote(index);
    }

    return {
      noteStore,
      addNote,
      deleteNote,
      setCurrentNote
    }
  },
  data() {
    return {
      isSidebarOpen: true,
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
@import url('https://fonts.googleapis.com/icon?family=Material+Icons+Outlined');

#canvas {
  display: flex;
  height: 100vh;
}

.navbar {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.toggle-sidebar-button,
.new-note-button {
  background: none;
  border: none;
  cursor: pointer;
  font-size: 24px;
  color: #666;
  transition: color 0.3s ease;
}

.toggle-sidebar-button:hover,
.new-note-button:hover {
  color: #007bff;
}

.material-icons {
  font-size: 24px;
}

.divider {
  border: none;
  height: 1px;
  background-color: #ddd;
  margin: 20px 0;
}

.sidebar {
  width: 250px;
  background-color: #f4f4f4;
  padding: 20px;
  transition: transform 0.3s ease;
  transform: translateX(-250px);
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
