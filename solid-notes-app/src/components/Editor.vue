<template>
  <div class="editor-container">
    <input v-model="title" placeholder="Title" class="title-input" />
    <quill-editor 
      v-model:content="content" 
      contentType="html" 
      :options="editorOptions" />
    <button @click="submitNote">Submit Note</button>
  </div>
</template>

<script>
import { QuillEditor } from '@vueup/vue-quill'
import '@vueup/vue-quill/dist/vue-quill.snow.css'
import axios from 'axios'

export default {
  components: { QuillEditor },
  data() {
    return {
      title: '',
      content: '',
      editorOptions: {
        modules: {
          toolbar: [
            ['bold', 'italic', 'underline'],
            ['blockquote', 'code-block'],
            [{ list: 'ordered' }, { list: 'bullet' }],
            [{ header: [1, 2, 3, false] }],
            [{ align: [] }],
            ['link', 'image'],
            ['clean'],
          ],
        },
        formats: [
          'bold', 'italic', 'underline',
          'blockquote', 'code-block',
          'list', 'bullet',
          'header',
          'align',
          'link', 'image',
        ],
        theme: 'snow',
        placeholder: 'Write your note here...',
      },
    }
  },
  methods: {
    getContent() {
      return this.content;
    },
    async submitNote() {
      console.log(this.title, this.content);
      try {
        const response = await axios.post('http://127.0.0.1:8000/notes/', {
          title: this.title,
          content: this.content,
        })
        console.log(response.data)
      } catch (error) {
        console.error('There was an error!', error)
      }
    }
  },
}
</script>

<style>
.editor-container {
  flex-grow: 1;
  display: flex;
  flex-direction: column;
}

.quill-editor {
  flex-grow: 1;
  display: flex;
  flex-direction: column;
}


/* Custom styles to remove borders */
.ql-container.ql-snow {
  border: none;
}

.ql-toolbar.ql-snow {
  border: none;
  display: flex;
  justify-content: center; /* Center align the toolbar */
}

.ql-editor {
  border: none;
  outline: none;
}

/* Styles for the title input */
.title-input {
  font-size: 24px; /* Large font size */
  border: none; /* Remove border */
  outline: none; /* Remove outline */
  width: 100%; /* Full width */
  margin: 25px 0px; /* Margin at the bottom */
  text-align: center; /* Center align text */
}
</style>
