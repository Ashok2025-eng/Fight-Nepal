from fastapi import FastAPI
import sqlite3
from pydantic import BaseModel

con = sqlite3.connect("fights.db", check_same_thread=False)

def initalize_databse():
    create_event_table = """
    CREATE TABLE events (
        eventName TEXT,
        participantOne TEXT,
        participantTwo TEXT,
        time TEXT,
        winner TEXT
    );
    """
    cursor=con.cursor()
    cursor.execute(create_event_table)

    initialize_database()
app = FastAPI()


@app.get("/")   
def main():
    return "flight-nepal"


class CreateEventRequest(BaseModel):
    eventName: str
    participantOne: str
    participantTwo: str
    time: str
    winner: str




@app.post("/event")
def create_event(event: CreateEventRequest):
    insertStatement = f"""
    INSERT INTO events (
        "eventName",
        "participantOne",
        "participantTwo",
        "time",
        "winner"
    )VALUES(
        {event.eventName},
        {event.participantOne},
        {event.participantTwo},
        {event.time},
        {event.winner}


        
    )
    """
    
    cursor = con.cursor()
    res = cursor.execute(insertStatement)
    affected = res.recount()
    print(f"Inserted {affected} rows in the database")
    con.commit


    return event


@app.get("/event/delete")
def delete_event():
    return "delete event"


@app.get("/event/get-all")
def get_all_events():
    get_statement = "SELECT* from events;"
    cursor = con.cursor()
    res = cursor.execute(get_statement)
    results = res.fetchall()
    return results


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
