from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String
from databases import Database

DATABASE_URL = "mysql+pymysql://root:root123@localhost/todo"
database = Database(DATABASE_URL)
engine = create_engine(DATABASE_URL)
metadata = MetaData()

students = Table(
    "students",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("name", String(50)),
    Column("classs", Integer)
)

todo_list = Table(
    "todo_list",
    metadata,
    Column("t_id", Integer, primary_key=True),
    Column("task", String(150)),
    Column("Date", Integer)
)

metadata.create_all(engine)

class Student(BaseModel): 
    id: int
    name: str
    classs: int  

class TodoList(BaseModel):  
    t_id: int
    task: str
    Date: int

app = FastAPI()

@app.on_event("startup")
async def startup():
    await database.connect()

@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()

@app.get("/students/")
async def read_students():
    query = students.select()
    return await database.fetch_all(query)

@app.get("/todo_list/")
async def read_todo_list():
    query = todo_list.select()
    return await database.fetch_all(query)

@app.get("/students/todolist/{id}")
async def read_student_by_name(id: int):
    query = students.select().where(students.c.id == id)
    student = await database.fetch_one(query)
    if student:
        return student
    else:
        raise HTTPException(status_code=404, detail="Student not found")

@app.post("/students/")
async def create_student_and_todo(student: Student, todo: TodoList):
    query_student = students.insert().values(
        id=student.id,
        name=student.name,
        classs=student.classs
    )
    await database.execute(query_student)

    query_todo = todo_list.insert().values(
        t_id=todo.t_id,
        task=todo.task,
        Date=todo.Date
    )
    await database.execute(query_todo)

    return {"message": "Student and Todo created successfully"}

@app.delete("/dl/students/{id}")
async def delete_student(id: int):
    query = students.delete().where(students.c.id == id)
    await database.execute(query)
    return {"message": "Student deleted successfully"}
