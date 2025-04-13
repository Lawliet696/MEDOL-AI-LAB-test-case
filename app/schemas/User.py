from pydantic import BaseModel


class CreateUserSchema(BaseModel):
    username: str
    password: str