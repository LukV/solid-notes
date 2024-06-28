import { defineStore } from 'pinia';
import { ref, watch } from 'vue';
import { getNotes, saveNotes as saveNotesToBackend } from '@/services/notesService';
import debounce from 'lodash.debounce';

export const useNoteStore = defineStore('noteStore', () => {
  const notes = ref([]);
  const currentNote = ref({ title: '', content: '<br>' });

  const loadNotes = async () => {
    try {
      const savedNotes = await getNotes();
      notes.value = savedNotes;
      sessionStorage.setItem('isNewNote', 'true');
    } catch (error) {
      console.error('Failed to load notes', error);
    }
  };

  const saveNotes = async () => {
    try {
      await saveNotesToBackend(notes.value);
    } catch (error) {
      console.error('Failed to save notes', error);
    }
  };

  const debouncedSaveNotes = debounce(saveNotes, 2000); // Adjust the delay as needed

  watch(notes, () => {
    debouncedSaveNotes();
  }, { deep: true });

  const addNote = () => {
    currentNote.value = { title: '', content: '<br>' };
    sessionStorage.setItem('isNewNote', 'true');
  };

  const submitNote = async () => {
    const newNote = { ...currentNote.value };
    notes.value.push(newNote);
    setCurrentNote(notes.value.length - 1);
    debouncedSaveNotes();
    sessionStorage.setItem('isNewNote', 'false');
  };

  const deleteNote = async (index) => {
    notes.value.splice(index, 1);
    currentNote.value = { title: '', content: '<br>' };
    debouncedSaveNotes();
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