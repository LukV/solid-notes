<template>
  <div id="canvas">
    <div :class="['sidebar', { open: isSidebarOpen }]">
      <h1>Solid Notes</h1>
      <nav>
        <ul>
          <li><a href="#" @click="createNote">Create Note</a></li>
          <li><a href="#" @click="deleteNote">Delete Note</a></li>
          <li><a href="#" @click="toggleSidebar">Toggle Sidebar</a></li>
        </ul>
        <ul>
          <li v-for="note in notes" :key="note.id"><a href="#">{{ note.title }}</a></li>
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

export default {
  name: 'App',
  components: {
    Editor
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
