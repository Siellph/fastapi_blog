from pydantic import BaseModel


class User(BaseModel):
    id: int
    username: str
    email: str

    class Config:
        orm_mode = True
        from_attributes = True


class UserLogin(BaseModel):
    username: str
    password: str


class UserLoginResponse(BaseModel):
    access_token: str
