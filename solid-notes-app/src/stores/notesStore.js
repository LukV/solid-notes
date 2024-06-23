import { defineStore } from 'pinia'
import { ref, watch } from 'vue'

export const useNoteStore = defineStore('note', () => {
  const notes = ref(JSON.parse(localStorage.getItem('notes')) || []);
  const currentNoteIndex = ref(-1);
  const currentNote = ref(createNewNote());
  const noteAdded = ref(false); // Flag to track if the note has been added

  function createNewNote() {
    return {
      title: '',
      content: '',
      date: new Date().toLocaleString()
    };
  }

  const addNote = () => {
    if (!currentNote.value.title.trim()) return; // Only add note if title is not empty
    const newNote = createNewNote();
    notes.value.push(newNote);
    setCurrentNote(notes.value.length - 1);
    noteAdded.value = true; // Set the flag when the note is added
  };

  const updateNote = (index, updatedNote) => {
    notes.value[index] = { ...updatedNote, date: new Date().toLocaleString() };
  };

  const deleteNote = (index) => {
    notes.value.splice(index, 1);
    if (currentNoteIndex.value === index) {
      resetCurrentNote();
    } else if (currentNoteIndex.value > index) {
      currentNoteIndex.value--;
    }
  };

  const resetCurrentNote = () => {
    currentNote.value = createNewNote();
    currentNoteIndex.value = -1;
    noteAdded.value = false; // Reset the flag
  };

  const loadNotes = () => {
    const savedNotes = localStorage.getItem('notes');
    if (savedNotes) {
      notes.value = JSON.parse(savedNotes);
    } else {
      localStorage.setItem('notes', JSON.stringify([]));
      addNote();
    }
  };

  const setCurrentNote = (index) => {
    currentNote.value = notes.value[index];
    currentNoteIndex.value = index;
    noteAdded.value = true; // Set the flag when an existing note is set
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

  watch(
    () => currentNote.value.title,
    (newTitle, oldTitle) => {
      if (!oldTitle && newTitle && !noteAdded.value) {
        addNote();
      }
    }
  );

  return {
    notes,
    currentNote,
    currentNoteIndex,
    addNote,
    updateNote,
    deleteNote,
    loadNotes,
    setCurrentNote,
    resetCurrentNote
  };
});
