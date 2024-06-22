import { defineStore } from 'pinia'
import { ref, watch } from 'vue'

export const useNoteStore = defineStore('note', () => {
  const notes = ref(JSON.parse(localStorage.getItem('notes')) || []);
  const newNote = ref({
    title: '',
    content: '',
    date: ''
  });

  const addNote = () => {
    newNote.value.date = new Date().toLocaleString();
    notes.value.push({ ...newNote.value });
    newNote.value = { title: '', content: '', date: '' };
  };

  const updateNote = (index, updatedNote) => {
    notes.value[index] = { ...updatedNote, date: new Date().toLocaleString() };
  };

  const deleteNote = (index) => {
    notes.value.splice(index, 1);
  };

  const loadNotes = () => {
    const savedNotes = localStorage.getItem('notes');
    if (savedNotes) {
      notes.value = JSON.parse(savedNotes);
    }
  };

  watch(
    notes,
    (newNotes) => {
      localStorage.setItem('notes', JSON.stringify(newNotes));
    },
    { deep: true }
  );

  watch(
    newNote,
    () => {
      localStorage.setItem('newNote', JSON.stringify(newNote.value));
    },
    { deep: true }
  );

  return {
    notes,
    newNote,
    addNote,
    updateNote,
    deleteNote,
    loadNotes
  };
});
