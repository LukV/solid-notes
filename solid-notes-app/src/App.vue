<template>
  <div id="canvas">
    <div :class="['sidebar', { open: isSidebarOpen }]">
      <h1>Solid Notes</h1>
      <button @click="addNote" class="new-note-button">Add note</button>
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
#canvas {
  display: flex;
  height: 100vh;
}

.new-note-button {
  display: block;
  width: 100%;
  padding: 10px 15px;
  font-size: 16px;
  color: #fff;
  background-color: #007bff;
  border: none;
  border-radius: 4px;
  text-align: center;
  cursor: pointer;
  transition: background-color 0.3s ease;
}

.new-note-button:hover {
  background-color: #0056b3;
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
