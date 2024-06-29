<template>
    <div class="sidebar-header">
        <button @click="$emit('toggle-sidebar')" class="toggle-sidebar-button">
            <span class="material-icons-outlined">view_sidebar</span>
        </button>
        <button @click="$emit('add-note')" class="new-note-button">
            <span class="material-icons-outlined">edit</span>
        </button>
    </div>
</template>

<script>
export default {
    name: 'SidebarHeader'
}
</script>

<style>
/* Include the necessary styles here */
.sidebar-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    height: 60px;
    padding: 0 15px;
    position: sticky;
    top: 0;
    z-index: 1;
    border-bottom: 1px solid #efefef;
}

.toggle-sidebar-button,
.new-note-button {
    background: none;
    border: none;
    cursor: pointer;
    color: #666;
    transition: color 0.3s ease;
}

.toggle-sidebar-button:hover,
.new-note-button:hover {
    color: #007bff;
}

.sidebar-header button:last-child {
    margin-right: 0;
}
</style>
