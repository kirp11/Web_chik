from pathlib import Path
from typing import Union, Dict, Annotated

from fastapi import FastAPI, HTTPException, status, Body, Query

app = FastAPI()

# TICKETS = [
#  {
#   "id": int,
#   "title": str,
#   "description": str,
#   "priority": str,
#   "status": str
#  }
# ]
# Ограничения:
# все поля - обязательные
# допустимые значения для поля "priority": "low", "medium", "high"
# допустимые значения для поля "status": "open", "in_progress", "closed"
#
#
# 1. Реализовать CRUD для тикетов.
# 2. Добавить фильтрацию:
# - GET /tickets?status=open
# - GET /tickets?priority=high
# 3. Добавить PUT /tickets/{id}/close — переводит статус в closed.

TICKETS = []
NEXT_ID = 1
PRIORITY_VALUES= ["low", "medium", "high"]
STATUS_VALUES= ["open", "in_progress", "closed"]

# 1. Реализовать CRUD для студентов.
@app.get("/tickets")
def get_tickets():
    return {
        "data": TICKETS
    }


@app.get("/tickets/{ticket_id}")
def get_ticket(ticket_id: int):
    ticket = next((ticket for ticket in TICKETS if ticket.get("id") == ticket_id), None)
    if ticket is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Ticket not found")
    return ticket


@app.post("/tickets/{title}/{description}/{priority}/{status}", status_code=status.HTTP_201_CREATED)
def create_ticket(title: str,
                   description: str,
                   priority: str = Path(description = "только значения из списка [low, medium, high]"),
                   status: str = Path(description = "только значения из списка [open, in_progress, closed]")):

    global NEXT_ID


    if priority not in PRIORITY_VALUES or status not in STATUS_VALUES:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_CONTENT, detail="Недопустимые значения")
    new_ticket = {
         "id": NEXT_ID,
          "title": title,
          "description": description,
          "priority": priority,
        "status": status,
    }
    TICKETS.append(new_ticket)
    NEXT_ID += 1
    return new_ticket


@app.put("/tickets/{id}")
def update_ticket(id: int, data: Dict[str, str| int]):

    for ticket in TICKETS:

        if ticket.get("id") == id:

            ticket["title"] = data.get("title")
            ticket["description"] = data.get("description")
            ticket["priority"] = data.get("priority")
            ticket["status"] = data.get("status")
            return ticket

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)


@app.delete("/tickets/{id}")
def delete_ticket(id: int):
    for ticket in TICKETS:
        if ticket.get("id") == id:
            del_ticket = ticket
            TICKETS.remove(ticket)
            return del_ticket

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)



# 2. Добавить фильтрацию:
# - GET /tickets?status=open
# - GET /tickets?priority=high

@app.get("/tickets/")
def get_еticket_filter(status: str = Query("open", description="Фильтр по статусу"),
              priority: str = Query("high", description="Фильтр по высокому приоритету")):

        filter_tickets = []
        for ticket in TICKETS:
            if ticket.get("status") == status and ticket.get("priority") == priority:
                filter_tickets.append(ticket)

        if not filter_tickets:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Tickets not found")
        return F"список билетов: {filter_tickets}"

# 3. Добавить PUT /tickets/{id}/close — переводит статус в closed.

@app.put("/tickets/{id}/close")
def close_ticket(id: int):

    for ticket in TICKETS:

        if ticket.get("id") == id:

            ticket["status"] = "closed"
            return ticket

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)