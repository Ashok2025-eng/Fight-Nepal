from fastapi import FastAPI
import sqlite3
from pydantic import BaseModel

# Connect to DB
con = sqlite3.connect("fights.db", check_same_thread=False)

# Initialize database
def initialize_database():
    create_event_table = """
    CREATE TABLE IF NOT EXISTS events (
        eventName TEXT,
        participantOne TEXT,
        participantTwo TEXT,
        time TEXT,
        winner TEXT
    );
    """
    cursor = con.cursor()
    cursor.execute(create_event_table)
    con.commit()

initialize_database()

app = FastAPI()


@app.get("/")
def main():
    return "fight-nepal"


class CreateEventRequest(BaseModel):
    eventName: str
    participantOne: str
    participantTwo: str
    time: str
    winner: str


@app.post("/event")
def create_event(event: CreateEventRequest):
    insert_statement = """
    INSERT INTO events (
        eventName,
        participantOne,
        participantTwo,
        time,
        winner
    ) VALUES (?, ?, ?, ?, ?)
    """
    cursor = con.cursor()
    cursor.execute(insert_statement, (
        event.eventName,
        event.participantOne,
        event.participantTwo,
        event.time,
        event.winner
    ))
    con.commit()

    return {"message": "Event created successfully", "event": event}


@app.delete("/event/delete/{eventName}")
def delete_event(eventName: str):
    delete_statement = "DELETE FROM events WHERE eventName = ?"
    cursor = con.cursor()
    cursor.execute(delete_statement, (eventName,))
    con.commit()
    return {"message": f"Event '{eventName}' deleted successfully"}


@app.get("/event/get-all")
def get_all_events():
    get_statement = "SELECT * FROM events"
    cursor = con.cursor()
    res = cursor.execute(get_statement)
    results = res.fetchall()
    return {"events": results}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
