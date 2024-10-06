#import extension
from fastapi import FastAPI
from fastapi import HTTPException , Depends
from pydantic import BaseModel
from sqlalchemy import  create_engine , MetaData , Column , Integer, String , Table, text
from sqlalchemy.orm import sessionmaker
from argon2 import PasswordHasher
from databases import Database
from datetime import timedelta
from fastapi_jwt_auth import AuthJWT , auth_jwt
import jwt
#data base setup
Database_URL = "mysql+pymysql://root:root123@localhost/pro"
database = Database(Database_URL)
engine = create_engine(Database_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
metadata = MetaData()
access_token = None
hashed_password = None
authjwt_secret_key = None

#SQL tables
users = Table (
    "users",
    metadata,
    Column("id", Integer ,primary_key = True ),
    Column ("name",String(100)),
    Column("email",String(200)),
    Column("password",String(200)),
    Column("Location",String(200)),
    Column("phone_no",Integer , unique=True)
)
booking = Table(
    "booking",
    metadata,
    Column(" b_id" ,Integer, primary_key=True),
    Column("destination",String(70)),
    Column("booking_date",Integer),
    Column("status",String(150))
)
reviews = Table(
    "reviews",
    metadata,
    Column("r_id",Integer,primary_key=True),
    Column("rating",Integer),
    Column("comments",String(100))
)
Hospatality = Table(
    "Hospatality",
    metadata,
    Column("h_id",String(150)), 
    Column("mess",String(150)),
    Column("hotel",String(150))
)
metadata.create_all(engine)
ph = PasswordHasher()
class users(BaseModel):
    name:str
    email:str
    password:str
    location:str
    phone_no:int
class booking(BaseModel):
    destination:str
    booking_date:int
    status:str
class reviews(BaseModel):
    rating:int
    comments:str
class hospatality(BaseModel):
    mess:str
    hotel:str
class login(BaseModel):
    email:str
    password:str
class Settings(BaseModel):
    authjwt_secret_key: str = "secret"
    authjwt_access_token_expires: timedelta = timedelta(minutes=50)
app = FastAPI()
@app.on_event("startup")
async def startup():
    await database.connect()
@app.on_event("shutdown")  
async def shutdown():
    await database.disconnect()
@AuthJWT.load_config
def get_config():
    return Settings()
def hash_password(password: str) -> str:
    users.password  = password
    return ph.hash(password)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
@app.post("/register")
async def register(user: users, database: SessionLocal = Depends(get_db)):
    hashed_password = hash_password(user.password)
    
    # Check if the email already exists
    query = text(f"SELECT * FROM users WHERE email = :email")
    existing_user = database.execute(query, {"email": user.email}).fetchone()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    # Insert new user into the database
    insert_query = text(
        "INSERT INTO users (name, phone_no, location, email, password) "
        f"VALUES ('{user.name}', '{user.phone_no}','{user.location}','{user.email}', '{hashed_password}')"
    )
    database.execute(insert_query, {
        "name": user.name,
        "phone_no": user.phone_no,
        "location": user.location,
        "email": user.email,
        "password": hashed_password
    })
    database.commit()
    return {"detail": "User registered successfully"}

@app.post("/login")
async def log(log: login, Authorize : AuthJWT = Depends()):
    global access_token 
    try:
        querry = f"Select password from users where email = '{log.email}'"
        result = await database.fetch_one(querry)
        correct = ph.verify(result.password,log.password)
        if correct :
            querry1 = f"select email from users where email = '{log.email}'"
            email = await database.fetch_one(querry1)
            access_token = Authorize.create_access_token(subject=str(email.email))
            return access_token
    except:
        raise HTTPException (status_code=404 , detail="user not registered")
@app.get("/me")
async def me(Authorize : AuthJWT =  Depends()):
    Authorize.jwt_required()
    decoded_token = jwt.decode(access_token,'secret',algorithms=["HS256"])
    try :
        query1 = f"Select name , email , location , phone_no from users where email = '{decoded_token.get("sub")}'  "
        result = await database.fetch_one(query1)
        return result , decoded_token
    except:
        raise HTTPException (status_code=404, detail="user not found")
@app.post("/create/booking")
async def book(book : booking,Authorize : AuthJWT = Depends(),db: SessionLocal = Depends(get_db)):
    Authorize.jwt_required()
    decoded_token = jwt.decode(access_token,'secret',algorithms=["HS256"])
    query = f"select id from users where email = '{decoded_token.get("sub")}'"
    id = await database.fetch_one(query)
    if id:   
        query4 = f"select b_id from booking where b_id = '{id.id}'"
        bid = await database.fetch_one(query4)
        if bid :
            raise HTTPException (status_code=404, detail=" user already register") 
        else:
            query1 = text(f"""INSERT INTO booking (b_id, destination , status , booking_date) VALUES('{id.id}','{book.destination}','{book.status}','{book.booking_date}')""")
            db.execute(query1,{
            "b_id":id,
            "destination" : book.destination,
            "status":book.status,
            "booking_date":book.booking_date
            }
            )
            db.commit()
            raise HTTPException (status_code=200 , detail="booking registered")
@app.delete("/delete/booking")
async def delet(Authorize : AuthJWT = Depends()):
    Authorize.jwt_required()
    decoded_token = jwt.decode(access_token,'secret',algorithms=["HS256"])
    query = f"select id from users where email = '{decoded_token.get("sub")}'"
    id = await database.fetch_one(query)
    query1 = f"delete from booking where b_id = '{id.id}'"
    result = await database.execute(query1)
    if result:
        raise HTTPException (status_code=200,detail="canceled booking")
@app.get("/booking")
async def get(Authorize : AuthJWT = Depends()):
    Authorize.jwt_required()
    decoded_token = jwt.decode(access_token,'secret',algorithms=["HS256"])
    query = f"select id from users where email = '{decoded_token.get("sub")}'"
    id = await database.fetch_one(query)
    if id:
        query1 = (f"select destination , booking_date , status from booking where b_id = '{id.id}' ")
        result = await database.fetch_all(query1)
        if result:
            return result
        raise HTTPException (status_code=404,detail="user not booked any trip")
@app.put("/update/booking")
async def update(book : booking,Authorize : AuthJWT = Depends(),db: SessionLocal = Depends(get_db)):
    Authorize.jwt_required()
    decoded_token = jwt.decode(access_token,'secret',algorithms=["HS256"])
    query = f"select id from users where email = '{decoded_token.get("sub")}'"
    id = await database.fetch_one(query)
    if id:   
        query4 = f"select b_id from booking where b_id = '{id.id}'"
        bid = await database.fetch_one(query4)
        if bid :
            query1 = text(f"update booking set destination = '{book.destination}' , status = '{book.status}', booking_date = '{book.booking_date}'")
            if booking.destination == "":
                raise HTTPException (status_code=200,detail="nothing to update")
            else:
                db.execute(query,{"destination" : book.destination,
                                "status" : book.status,
                                "booking_date ": book.booking_date}) 
                db.commit()           
                return ("updated")
        else:
            raise HTTPException (status_code=404, detail=" user not  booked") 

# #route for reviews
# @app.get("/reviews")
# async def reviews(Authorize : AuthJWT = Depends()):
#     query 