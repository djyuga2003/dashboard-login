import jwt
import uvicorn
from fastapi import FastAPI
from fastapi.encoders import jsonable_encoder
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

SECERT_KEY = "my_secret_key"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRES_MINUTES = 800

test_user = {
    "username": "temitope",
    "password": "temipassword",

}

app = FastAPI()

origins = {
    "http://localhost",
    "http://localhost:3000",
}

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class LoginItem(BaseModel):
    username: str
    password: str

    @app.get("/")
    def read_root(self):
        return {"Hello": "World"}


@app.post("/login")
async def user_login(loginitem: LoginItem):
    data = jsonable_encoder(loginitem)

    if data['username'] == test_user['username'] and data['password'] == test_user['password']:

        encoded_jwt = jwt.encode(data, SECERT_KEY, algorithm=ALGORITHM)
        return {'token': encoded_jwt}
    else:
        return {'message': 'login failed'}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000, log_level="info")