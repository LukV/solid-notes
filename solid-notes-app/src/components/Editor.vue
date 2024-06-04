<template>
  <div>
    <input v-model="title" placeholder="Title" />
    <quill-editor v-model:content="content" contentType="html" />
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
  