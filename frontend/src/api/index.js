// frontend/src/api/index.js

import axios from 'axios';

// 建立 Axios 實例，並設定後端 API 的基礎 URL
const apiClient = axios.create({
  baseURL: 'http://127.0.0.1:8000/api', // 你的後端 API 地址
  headers: {
    'Content-Type': 'application/json',
  },
});

export default {
  getTodos() {
    return apiClient.get('/todos');
  },
  addTodo(todo) {
    return apiClient.post('/todos', todo);
  },
  updateTodo(id, todo) {
    return apiClient.put(`/todos/${id}`, todo);
  },
  deleteTodo(id) {
    return apiClient.delete(`/todos/${id}`);
  },
};