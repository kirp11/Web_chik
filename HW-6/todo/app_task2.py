from pathlib import Path
from typing import Union, Dict, Annotated

from fastapi import FastAPI, HTTPException, status, Body, Query

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

STUDENTS = []
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
def create_student(group: str, name: str, data: Dict[str, Union[str, int, list]] = Body(...)):

    global NEXT_ID

    grades = data.get("grades")
    for grade in grades:
        if grade.get("value")<1 or grade.get("value")>5:
            raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_CONTENT)
    new_student = {
         "id": NEXT_ID,
          "name": name,
          "group": group,
          "grades": grades
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

@app.get("/students/{id}/avg-grade")
def get_student_avg_grade(student_id: int):
    student = next((student for student in STUDENTS if student.get("id") == student_id), None)
    if student is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Student not found")
    grades = student.get("grades")
    summ = 0
    n = 0
    for grade in grades:
        summ += grade.get("value")
        n+=1
    avg_grade = summ/n

    return f"средний балл студента по предметам {avg_grade}"

# 3. Добавить фильтрацию GET /students?group=IVT-101 — фильтрация по группе.

@app.get("/students/")
def get_group(group: str = Query(None, description="Фильтр по группе")):
    if group:
        group_students = []
        for student in STUDENTS:
            if student.get("group") == group:
                group_students.append(student)

        if not group_students:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Group not found")
        return F"список студентов из группы {group}: {group_students}"
    return STUDENTS