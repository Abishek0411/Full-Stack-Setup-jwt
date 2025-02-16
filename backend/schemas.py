from pydantic import BaseModel, EmailStr

# Schema for user registration input validation
class UserCreate(BaseModel):
    username: str   # Ensure username is a string
    email: EmailStr   # Validate email format
    password: str   # Store raw password before hashing