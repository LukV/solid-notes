import { defineStore } from 'pinia'
import { ref, watch } from 'vue'

export const useNoteStore = defineStore('note', () => {
  const notes = ref(JSON.parse(localStorage.getItem('notes')) || []);
  const currentNoteIndex = ref(-1);
  const currentNote = ref(createNewNote());

  function createNewNote() {
    return {
      title: '',
      content: '',
      date: new Date().toLocaleString()
    };
  }

  const addNote = () => {
    const newNote = createNewNote();
    notes.value.push(newNote);
    setCurrentNote(notes.value.length - 1);
  };

  const updateNote = (index, updatedNote) => {
    notes.value[index] = { ...updatedNote, date: new Date().toLocaleString() };
  };

  const deleteNote = (index) => {
    notes.value.splice(index, 1);
    if (currentNoteIndex.value === index) {
      currentNote.value = createNewNote();
      currentNoteIndex.value = -1;
    } else if (currentNoteIndex.value > index) {
      currentNoteIndex.value--;
    }
  };

  const loadNotes = () => {
    const savedNotes = localStorage.getItem('notes');
    if (savedNotes) {
      notes.value = JSON.parse(savedNotes);
    } 
  };

  const setCurrentNote = (index) => {
    currentNote.value = notes.value[index];
    currentNoteIndex.value = index;
  };

  watch(
    notes,
    (newNotes) => {
      localStorage.setItem('notes', JSON.stringify(newNotes));
    },
    { deep: true }
  );

  watch(
    currentNote,
    (newCurrentNote) => {
      if (currentNoteIndex.value >= 0) {
        notes.value[currentNoteIndex.value] = newCurrentNote;
      }
      localStorage.setItem('currentNote', JSON.stringify(currentNote.value));
    },
    { deep: true }
  );

  return {
    notes,
    currentNote,
    currentNoteIndex,
    addNote,
    updateNote,
    deleteNote,
    loadNotes,
    setCurrentNote
  };
});
