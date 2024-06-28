import { defineStore } from 'pinia';
import { ref } from 'vue';

export const useNoteStore = defineStore('noteStore', () => {
  const notes = ref([]);
  const currentNote = ref({ title: '', content: '<br>' });

  const loadNotes = () => {
    const savedNotes = localStorage.getItem('notes');
    notes.value = savedNotes ? JSON.parse(savedNotes) : [];
    sessionStorage.setItem('isNewNote', 'true');
  };

  const saveNotes = () => {
    localStorage.setItem('notes', JSON.stringify(notes.value));
  };

  const addNote = () => {
    currentNote.value = { title: '', content: '<br>' };
    sessionStorage.setItem('isNewNote', 'true');
  };

  const submitNote = () => {
    const newNote = { ...currentNote.value };
    notes.value.push(newNote);
    setCurrentNote(notes.value.length - 1);
    saveNotes();
    sessionStorage.setItem('isNewNote', 'false');
  };

  const deleteNote = (index) => {
    notes.value.splice(index, 1);
    currentNote.value = { title: '', content: '<br>' };
    saveNotes();
    sessionStorage.setItem('isNewNote', 'true');
  };

  const setCurrentNote = (index) => {
    currentNote.value = notes.value[index];
    sessionStorage.setItem('isNewNote', 'false');
  };

  return {
    notes,
    currentNote,
    loadNotes,
    addNote,
    saveNotes,
    submitNote,
    deleteNote,
    setCurrentNote,
  };
});