from fastapi import FastAPI, HTTPException, Depends
from fastapi_jwt_auth import AuthJWT
from fastapi_jwt_auth.exceptions import AuthJWTException
from pydantic import BaseModel
from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String, text
from sqlalchemy.orm import sessionmaker
from argon2 import PasswordHasher
from databases import Database
from fastapi.staticfiles import StaticFiles
from datetime import timedelta
import jwt
# Database setup
DATABASE_URL = "mysql+pymysql://root:root123@localhost/login"
database = Database(DATABASE_URL)
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
metadata = MetaData()
access_token = None
hashed_password =None
authjwt_secret_key = None
# MySQL table definition
users = Table(
    "users",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("name", String(50)),
    Column("office", String(100)),
    Column("hire_date", String(100)),
    Column("address", String(255)),
    Column("email", String(255), unique=True),
    Column("password", String(200)),
)
todo = Table(
    "todo",
    metadata,
    Column("id_todo",Integer,primary_key=True),
    Column("tasks", String(45))
)
metadata.create_all(engine)
ph = PasswordHasher() # hashing lib object
# Hashing password
class todo(BaseModel):
    todo_id : int
    task : str
class User(BaseModel):
    name: str
    office: str
    hire_date: str
    address: str
    email: str
    password: str

class Settings(BaseModel):
    authjwt_secret_key: str = "secret"
    authjwt_access_token_expires: timedelta = timedelta(minutes=5)
class UserLogin(BaseModel):
    email: str
    password: str 

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
@app.on_event("startup")
async def startup():
    await database.connect()
@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()
# Authentication
@AuthJWT.load_config
def get_config():
    return Settings()
def hash_password(password: str) -> str:
    return ph.hash(password)
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
# Dependency to get DB session
# Register route
@app.post("/register")
async def register(user: User, database: SessionLocal = Depends(get_db)):
    hashed_password = hash_password(user.password)
    # Check if user already exists
    query = text(f"SELECT * FROM users WHERE email = '{user.email}'")
    existing_user = database.execute(query, {"email": user.email}).fetchone()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    #Insert the new user
    insert_query = text(f"""
        INSERT INTO users (name, office, hire_date, address, email, password)
        VALUES ('{user.name}', '{user.office}', '{user.hire_date}', '{user.address}', '{user.email}','{hashed_password}')
    """)
    database.execute(insert_query, {
        "name": user.name,
        "office": user.office,
        "hire_date": user.hire_date,
        "address": user.address,
        "email": user.email,
        "password": hashed_password
    })
    database.commit()
    raise HTTPException(status_code=200, detail="User registered successfully") 
@app.post("/login")
async def login(User: UserLogin, Authorize: AuthJWT = Depends()):
    global access_token
    try:
        query = f"SELECT password FROM users where email = '{User.email}'"
        passw = await database.fetch_one(query)
        correct = ph.verify(passw.password, User.password)
        if correct:
            try:
                queryy = text(f"SELECT email FROM users WHERE email = '{User.email}'")
                result = await database.fetch_one(queryy)
                access_token = Authorize.create_access_token(subject=str(result.email))
                return access_token
            except Exception as e:
                print(f"Error during token creation: {str(e)}")
                return "Error during token creation"
        else:
            return "invalid hash error"
    
    except Exception as e:
        print(f"Password verification failed: {str(e)}")
        return "password is incorrect"
# Secure routes with JWT
@app.get("/me")
async def me(Authorize: AuthJWT = Depends()):
    Authorize.jwt_required()
    decoded_token = jwt.decode(access_token,'secret',algorithms=["HS256"])
    query = (f"Select name ,email,password, office, hire_date From users where email = '{decoded_token.get("sub")}'")
    return await database.fetch_one(query) , decoded_token 
@app.get("/users/")
async def read_users(Authorize: AuthJWT = Depends()):
    Authorize.jwt_required()
    query = text("SELECT name , office, email, hire_date,address FROM users")
    result = await database.fetch_all(query)
    return result
@app.get("/users/{name}")
async def get_user_by_name(name: str, Authorize: AuthJWT = Depends()):
    Authorize.jwt_required()
    try:
        query = text(f"SELECT name, office, hire_date, address, email FROM users WHERE name LIKE '{name}%'")
        result = await database.fetch_one(query)
        if result is None:
            raise HTTPException(status_code=404, detail="user not found")
        return result
    except Exception as e:
        raise HTTPException(status_code=404, detail="user not found") from e

@app.delete("/delete/")
async def delete_user(Authorize: AuthJWT = Depends()):
    Authorize.jwt_required()
    decoded_token = jwt.decode(access_token,'secret',algorithms=["HS256"])
    email =  decoded_token.get("sub")
    query = text(f"DELETE FROM users WHERE email = '{email}'")
    result = await database.execute(query)
    if result :
        return {f"Successfully deleted user {email}"}
    else:
        raise HTTPException (status_code=417)
@app.put("/update/{message}")
async def update_user(user: User,message:str, Authorize: AuthJWT = Depends(), database: SessionLocal = Depends(get_db)):
    Authorize.jwt_required()
    decoded_token = jwt.decode(access_token,'secret',algorithms=["HS256"])
    email =  decoded_token.get("sub")
    if message  == 'name':
        query = text(f"UPDATE users SET name = '{user.name}' where email = '{email}'")
        if user.name == "":# update name
            return "previous value saved"
        else:
            database.execute(query,{"name" : user.name}) 
            database.commit()           
            return ("updated,")
    elif message == 'office':# update office
        query = text(f"""UPDATE users SET office = '{user.office}' where email = '{email}'""")
        if user.office == "":
            return "previous value saved"    
        else:
            database.execute(query, {"office" : user.office} )
            database.commit()
            return "updated"
    elif message == 'password':#update password
        query = text(f"""UPDATE users SET password = '{user.password}' where email = '{email}'""")
        if user.password == "":
            return "previous value saved"
        else:
            database.execute(query, {"password" : ph.hash(user.password)})
            database.commit()
            return "updated"
    elif message == 'address':# update address
        query = text(f"""UPDATE users SET address = '{user.address}' where email = '{email}'""")
        if user.address == "":
            return "previous value saved"
        else:
            database.execute(query, {"address" : user.address})
            database.commit()
            return "updated"
    elif message == 'hire_date':# update hire_date
        query = text(f"""UPDATE users SET hire_date = '{user.hire_date}' where email = '{email}'""")
        if user.hire_date == "":
            return "previous value saved"
        else:
            database.execute(query, {"hiredate" : user.hire_date})
            database.commit()
            return "updated"
    elif message == 'email':#update email
        query = text(f"""UPDATE users SET email = '{user.email}' where email = '{email}'""")
        if user.email == "":
            return "previous value saved"
        else:
            database.execute(query, {"email" : user.email})
            database.commit()
            return "updated"
@app.get("/todo")
async def todo(Authorize: AuthJWT = Depends()):
    Authorize.jwt_required()
    decoded_token = jwt.decode(access_token,'secret',algorithms=["HS256"])
    email =  decoded_token.get("sub")
    query1 = (f"SELECT u.id, t.tasks FROM users u JOIN todo t ON u.id = t.id_todo ")
    result = await database.fetch_one(query1)
    return result

    # yha pr task mangwany hain class todo se todolist k liye or join lagana he users or todo table ka email k zariye 