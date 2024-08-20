from typing import Union
from fastapi import FastAPI
user_db={
'rooh' : {'name : rooh','office: deve','data : 24-april'},
'haris' : {'name : haris','office : qa','data : 22-april'},
'jack' : {'name : jack','office : qa','data : 25-april'}
}
app = FastAPI()
@app.get("/users")
def get_users():
    user_list = list(user_db.values())
    return user_list
@app.get("/users/{limit}")
def get_users_name(limit : int):
    user_list = list(user_db.values())
    return user_list[:limit]
