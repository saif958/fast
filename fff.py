from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String
from databases import Database

DATABASE_URL = "mysql+pymysql://root:root123@localhost/db"
database = Database(DATABASE_URL)
engine = create_engine(DATABASE_URL)
metadata = MetaData()

users = Table(
    "users",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("name", String(50)),
    Column("office", String(100)),
    Column("hire_date", String(100)),
    Column("address", String(255)),
)

metadata.create_all(engine)

class User(BaseModel):
    name: str
    office: str
    hire_date: str  
    address: str

app = FastAPI()

@app.on_event("startup")
async def startup():
    await database.connect()

@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()

@app.get("/users/")
async def read_users():
    query = users.select()
    return await database.fetch_all(query)

@app.get("/users/{name}")
async def get_user_by_name(name: str):
    query = users.select().where(users.c.name == name)
    user = await database.fetch_one(query)
    if user:
        return user
    else:
        raise HTTPException(status_code=404, detail="User not found")

@app.post("/users/")
async def create_user(user: User):
    query = users.insert().values(
        name=user.name,
        office=user.office,
        hire_date=user.hire_date,
        address=user.address
    )
    await database.execute(query)
    return {"message": "User created successfully"}

@app.delete("/users/{name}")
async def delete_user(name: str):
    query = users.delete().where(users.c.name == name)
    result = await database.execute(query)
    if result:
        return {"message": f"Successfully deleted user {name}"}
    else:
        raise HTTPException(status_code=404, detail="User not found")

@app.put("/users/{name}")
async def update_user(name: str, user: User):
    query = users.update().where(users.c.name == name).values(
        office=user.office,
        hire_date=user.hire_date,
        address=user.address
    )
    result = await database.execute(query)
    if result:
        return {"message": f"Successfully updated user {name}"}
    else:
        raise HTTPException(status_code=404, detail="User not found")
