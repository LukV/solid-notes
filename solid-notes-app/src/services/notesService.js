// Mock notes data for initial testing
const mockNotes = [
    { title: 'Sample Note 1', content: '<p>Content of Sample Note 1</p>' },
    { title: 'Sample Note 2', content: '<p>Content of Sample Note 2</p>' },
  ];
  
// Simulate delay for async operations
const delay = (ms) => new Promise((resolve) => setTimeout(resolve, ms));

export const getNotes = async () => {
    await delay(500); // Simulate network delay
    return mockNotes;
};

export const saveNotes = async (notes) => {
    await delay(500); // Simulate network delay
    console.log('Notes saved to backend:', notes);
};
  