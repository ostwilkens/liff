#%%
from fastapi import Request, FastAPI
import sqlite3
import uvicorn

# create table
conn = sqlite3.connect("store.sqlite")
c = conn.cursor()
c.execute("CREATE TABLE IF NOT EXISTS machine_activity (time INT, frequency INT, input_count INT, os TEXT, platform TEXT, release TEXT, node TEXT)")
c.execute("CREATE TABLE IF NOT EXISTS window_focus (time INT, title TEXT, process TEXT, description TEXT, os TEXT, platform TEXT, release TEXT, node TEXT)")
conn.commit()
conn.close()

api = FastAPI()

@api.get("/")
def read_root():
    return "It works!"

@api.post("/add_machine_activity")
async def add_machine_activity(request: Request):
    activity = await request.json()
    conn = sqlite3.connect("store.sqlite")
    c = conn.cursor()
    c.execute("INSERT INTO machine_activity VALUES (?,?,?,?,?,?,?)", (activity["time"], activity["frequency"], activity["input_count"], activity["os"], activity["platform"], activity["release"], activity["node"]))
    conn.commit()
    conn.close()
    return "OK"

@api.post("/add_window_focus")
async def add_window_focus(request: Request):
    focus = await request.json()
    conn = sqlite3.connect("store.sqlite")
    c = conn.cursor()
    c.execute("INSERT INTO window_focus VALUES (?,?,?,?,?,?,?,?)", (focus["time"], focus["title"], focus["process"], focus["description"], focus["os"], focus["platform"], focus["release"], focus["node"]))
    conn.commit()
    conn.close()
    return "OK"
