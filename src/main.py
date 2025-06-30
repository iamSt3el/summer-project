import uuid
from datetime import datetime
from typing import Optional

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI(title="Task Management API", version="1.0.0")

class Task(BaseModel):
    id: str
    title: str
    description: Optional[str] = None
    completed: bool = False
    created_at: datetime

class TaskCreate(BaseModel):
    title: str
    description: Optional[str] = None

class TaskUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    completed: Optional[bool] = None

tasks: list[Task] = []

@app.get("/")
def read_root():
    return {"message": "Task Management API", "version": "1.0.0"}

@app.get("/tasks", response_model=list[Task])
def get_tasks():
    return tasks

@app.post("/tasks", response_model=Task)
def create_task(task: TaskCreate):
    new_task = Task(
        id=str(uuid.uuid4()),
        title=task.title,
        description=task.description,
        completed=False,
        created_at=datetime.now()
    )
    tasks.append(new_task)
    return new_task

@app.get("/tasks/{task_id}", response_model=Task)
def get_task(task_id: str):
    for task in tasks:
        if task.id == task_id:
            return task
    raise HTTPException(status_code=404, detail="Task not found")

@app.put("/tasks/{task_id}", response_model=Task)
def update_task(task_id: str, task_update: TaskUpdate):
    for i, task in enumerate(tasks):
        if task.id == task_id:
            if task_update.title is not None:
                task.title = task_update.title
            if task_update.description is not None:
                task.description = task_update.description
            if task_update.completed is not None:
                task.completed = task_update.completed
            tasks[i] = task
            return task
    raise HTTPException(status_code=404, detail="Task not found")

@app.delete("/tasks/{task_id}")
def delete_task(task_id: str):
    for i, task in enumerate(tasks):
        if task.id == task_id:
            del tasks[i]
            return {"message": "Task deleted successfully"}
    raise HTTPException(status_code=404, detail="Task not found")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
