from pathlib import Path
from typing import Union, Dict, Annotated

from fastapi import FastAPI, HTTPException, status

app = FastAPI()

# Данные: простая база студентов.
#
# Ограничения:
# поле "value" внутри "grades" может содержать значение только от 1 до 5
# "name" и "group" - обязательные поля для студентов
#
# 1. Реализовать CRUD для студентов.
# 2. Добавить маршрут GET /students/{id}/avg-grade — вернуть средний балл.
# 3. Добавить фильтрацию GET /students?group=IVT-101 — фильтрация по группе.
#

STUDENTS = [
 {
  "id": int,
  "name": str,
  "group": str,
  "grades": [
   {
    "subject": str,
    "value": int
   }
  ]
 }
]
NEXT_ID = 1


# 1. Реализовать CRUD для студентов.
@app.get("/students")
def get_students():
    return {
        "data": STUDENTS
    }


@app.get("/students/{student_id}")
def get_student(student_id: int):
    student = next((student for student in STUDENTS if student.get("id") == student_id), None)
    if student is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Student not found")
    return student


@app.post("/students/{group}/{name}", status_code=status.HTTP_201_CREATED)
def create_student(data: Dict[str, str|int]):

    global NEXT_ID

    value = data.get("grades[value]")
    if value <1 and value>5:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    new_student = {
         "id": data.get("id"),
          "name": data.get("name"),
          "group": data.get("group"),
          "grades": [
           {
            "subject": data.get("grades[subject]"),
            "value": data.get("grades[value]"),
           }
          ]
    }
    STUDENTS.append(new_student)
    NEXT_ID += 1
    return new_student


@app.put("/students/{id}")
def update_todo(id: int, data: Dict[str, str| int]):

    for student in STUDENTS:

        if student.get("id") == id:

            student["group"] = data.get("group")
            student["grades"] = data.get("grades")
            return student

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)


@app.delete("/students/{id}")
def delete_student(id: int):
    for student in STUDENTS:
        if student.get("id") == id:
            del_stud = student
            STUDENTS.remove(student)
            return del_stud

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

# 2. Добавить маршрут GET /students/{id}/avg-grade — вернуть средний балл.



# 3. Добавить фильтрацию GET /students?group=IVT-101 — фильтрация по группе.