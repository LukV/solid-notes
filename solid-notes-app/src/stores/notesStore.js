import { defineStore } from 'pinia'
import axios from 'axios'

export const useNoteStore = defineStore('note', {
  state: () => ({
    title: localStorage.getItem('noteTitle') || '',
    content: localStorage.getItem('noteContent') || '',
  }),
  actions: {
    updateTitle(newTitle) {
      this.title = newTitle;
      localStorage.setItem('noteTitle', newTitle);
    },
    updateContent(newContent) {
      this.content = newContent;
      localStorage.setItem('noteContent', newContent);
    }
  }
})
