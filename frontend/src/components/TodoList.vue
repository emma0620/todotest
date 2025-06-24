<template>
  <el-card class="box-card" shadow="never">
    <template #header>
      <div class="flex justify-between items-center">
        <span class="text-xl font-semibold">我的待辦事項</span>
      </div>
    </template>

    <!-- 新增區塊 -->
    <div class="flex mb-6">
      <el-input
        v-model="newTodoTitle"
        placeholder="請輸入新的待辦事項"
        @keyup.enter="addTodo"
        clearable
        size="large"
        class="flex-grow mr-4"
      />
      <el-button type="primary" @click="addTodo" size="large">新增</el-button>
    </div>

    <!-- 列表區塊 -->
    <el-table :data="todos" v-loading="isLoading" stripe style="width: 100%">
      <el-table-column label="狀態" width="100">
        <template #default="scope">
          <el-switch
            v-model="scope.row.completed"
            @change="() => updateTodoStatus(scope.row)"
          />
        </template>
      </el-table-column>

      <el-table-column label="標題">
        <template #default="scope">
          <span :class="{ 'line-through text-gray-400': scope.row.completed }">
            {{ scope.row.title }}
          </span>
        </template>
      </el-table-column>

      <el-table-column label="操作" width="120" align="right">
        <template #default="scope">
          <el-button
            type="danger"
            size="small"
            @click="deleteTodo(scope.row)"
            circle
            plain
          >
            <el-icon><Delete /></el-icon>
          </el-button>
        </template>
      </el-table-column>
    </el-table>
    <el-empty
      v-if="!isLoading && todos.length === 0"
      description="太棒了，沒有待辦事項！"
    />
  </el-card>
</template>
<script setup>
import { ref, onMounted } from "vue";
import api from "../api";
import { ElMessage, ElMessageBox } from "element-plus";

// 響應式狀態
const todos = ref([]);
const newTodoTitle = ref("");
const isLoading = ref(true);

// --- API 方法 ---

// 獲取所有 todos
const fetchTodos = async () => {
  try {
    isLoading.value = true;
    const response = await api.getTodos();
    todos.value = response.data;
  } catch (error) {
    console.error("獲取 todos 失敗:", error);
    ElMessage.error("無法載入待辦事項列表");
  } finally {
    isLoading.value = false;
  }
};

// 新增 todo
const addTodo = async () => {
  if (!newTodoTitle.value.trim()) {
    ElMessage.warning("標題不能為空");
    return;
  }
  try {
    const newTodo = { title: newTodoTitle.value, completed: false };
    const response = await api.addTodo(newTodo);
    todos.value.push(response.data);
    newTodoTitle.value = "";
    ElMessage.success("新增成功！");
  } catch (error) {
    console.error("新增 todo 失敗:", error);
    ElMessage.error("新增失敗，請稍後再試");
  }
};

// 更新 todo 狀態
const updateTodoStatus = async (todo) => {
  try {
    // 這裡我們只更新 completed 狀態
    const updatedData = { completed: todo.completed };
    await api.updateTodo(todo.id, updatedData);
    ElMessage.success(`'${todo.title}' 狀態已更新`);
  } catch (error) {
    console.error("更新 todo 狀態失敗:", error);
    ElMessage.error("更新狀態失敗");
    // 如果更新失敗，將狀態恢復
    todo.completed = !todo.completed;
  }
};

// 刪除 todo
const deleteTodo = async (todo) => {
  try {
    await ElMessageBox.confirm(`確定要刪除 '${todo.title}' 嗎？`, "警告", {
      confirmButtonText: "確定",
      cancelButtonText: "取消",
      type: "warning",
    });

    await api.deleteTodo(todo.id);
    todos.value = todos.value.filter((t) => t.id !== todo.id);
    ElMessage.success("刪除成功！");
  } catch (error) {
    // 如果用戶點擊取消，error 會是 'cancel'，我們不需要顯示錯誤訊息
    if (error !== "cancel") {
      console.error("刪除 todo 失敗:", error);
      ElMessage.error("刪除失敗");
    }
  }
};

// 組件掛載時，獲取初始資料
onMounted(() => {
  fetchTodos();
});
</script>

<style scoped>
/* scoped CSS 確保樣式只作用於此組件 */
.box-card {
  border-radius: 12px;
  border: 1px solid #e2e8f0;
}
.line-through {
  text-decoration: line-through;
}
</style>
