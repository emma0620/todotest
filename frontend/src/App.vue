<!-- frontend/src/App.vue -->
<script setup>
import TodoList from "./components/TodoList.vue";
</script>

<template>
  <div class="bg-gray-100 min-h-screen font-sans">
    <header class="bg-blue-600 text-white p-4 shadow-md">
      <h1 class="text-3xl font-bold text-center">全端 Todo List 練習</h1>
      <p class="text-center text-blue-200">
        Vue 3 + Element Plus + Tailwind CSS + Python FastAPI
      </p>
    </header>
    <main class="container mx-auto mt-8 p-4">
      <TodoList />
    </main>
  </div>
</template>

<style>
.container {
  max-width: 800px;
}
</style>
