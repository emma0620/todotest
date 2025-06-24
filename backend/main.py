# backend/main.py

from fastapi import FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional

# 建立 FastAPI 應用實例
app = FastAPI()

# --- CORS 中介軟體設定 ---
# 為了允許前端 (例如 http://localhost:5173) 能夠訪問我們的後端 API
# 這是前後端分離專案的關鍵步驟
origins = [
    "http://localhost:5173",  # Vue 開發伺服器的預設地址
    "http://127.0.0.1:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],  # 允許所有 HTTP 方法
    allow_headers=["*"],  # 允許所有 HTTP 標頭
)


# --- 資料模型 (Pydantic Models) ---
# 定義 Todo 項目的資料結構
class TodoBase(BaseModel):
    title: str
    completed: bool = False


class TodoCreate(TodoBase):
    pass


class TodoUpdate(BaseModel):
    title: Optional[str] = None
    completed: Optional[bool] = None


class TodoInDB(TodoBase):
    id: int


# --- 模擬資料庫 ---
# 為了簡化，我們使用一個 Python list 來當作記憶體資料庫
# 伺服器重啟後資料會消失，這對於練習來說是 OK 的
db_todos: List[TodoInDB] = [
    TodoInDB(id=1, title="學習 Vue 3", completed=True),
    TodoInDB(id=2, title="學習 FastAPI", completed=False),
    TodoInDB(id=3, title="整合 Element Plus 與 TailwindCSS", completed=False),
]
next_id = 4


# --- API 端點 (Endpoints) ---


# 根路徑
@app.get("/")
def read_root():
    return {"message": "歡迎來到 Todo List API"}


# 獲取所有 Todo 項目
@app.get("/api/todos", response_model=List[TodoInDB])
def get_todos():
    return db_todos


# 新增一個 Todo 項目
@app.post("/api/todos", response_model=TodoInDB, status_code=status.HTTP_201_CREATED)
def create_todo(todo: TodoCreate):
    global next_id
    new_todo = TodoInDB(id=next_id, title=todo.title, completed=todo.completed)
    db_todos.append(new_todo)
    next_id += 1
    return new_todo


# 更新一個 Todo 項目
@app.put("/api/todos/{todo_id}", response_model=TodoInDB)
def update_todo(todo_id: int, todo_update: TodoUpdate):
    for index, todo in enumerate(db_todos):
        if todo.id == todo_id:
            # 更新資料
            if todo_update.title is not None:
                db_todos[index].title = todo_update.title
            if todo_update.completed is not None:
                db_todos[index].completed = todo_update.completed
            return db_todos[index]
    raise HTTPException(status_code=404, detail="Todo not found")


# 刪除一個 Todo 項目
@app.delete("/api/todos/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_todo(todo_id: int):
    global db_todos
    todo_to_delete = next((todo for todo in db_todos if todo.id == todo_id), None)
    if not todo_to_delete:
        raise HTTPException(status_code=404, detail="Todo not found")
    db_todos = [todo for todo in db_todos if todo.id != todo_id]
    return
