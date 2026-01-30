from pydantic import BaseModel

class LoginSchema(BaseModel):
    username: str
    password: str

class UserSchema(BaseModel):
    jwt_token: str

class SignupSchema(BaseModel):
    username: str
    password: str  
    confirmPassword: str

class UpdateYearGroupSchema(BaseModel):
    jwt_token: str
    year_group: int