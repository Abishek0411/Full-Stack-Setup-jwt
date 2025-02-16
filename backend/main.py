from fastapi import FastAPI, HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi.middleware.cors import CORSMiddleware
from database import get_connection
from schemas import UserCreate
import bcrypt   # Library for password hashing
from jose import jwt   # This is for python-jose  # Library for JSON Web Token (JWT)
import datetime
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = FastAPI()     # Create FastAPI instance

# CORS middleware to allow requests from React
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # Allow the React frontend
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Secret key for JWT
SECRET_KEY = os.getenv("JWT_SECRET")
ALGORITHM = "HS256"

# FastAPI's OAuth2 scheme for token authentication
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

# Function to hash passwords before storing in the database
def hash_password(password: str) -> str:
    salt = bcrypt.gensalt()     # Generate a random salt
    hashed_pw = bcrypt.hashpw(password.encode('utf-8'), salt)   # Hash the password
    return hashed_pw.decode('utf-8')    # Convert bytes to string for storage

# Function to verify passwords
def verify_password(plain_password, hashed_password):
    return bcrypt.checkpw(plain_password.encode('utf-8'), hashed_password.encode('utf-8'))

# Function to generate a JWT token
def create_access_token(data: dict, expires_delta: datetime.timedelta):
    to_encode = data.copy()
    expire = datetime.datetime.now(datetime.timezone.utc) + expires_delta
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

# API endpoint to register a new user
@app.post("/register")
def register_user(user: UserCreate):
    try:
        conn = get_connection()
        if conn is None:
            raise HTTPException(status_code=500, detail="Database Connection Error")
        
        cursor = conn.cursor()

        # Check if the username or email already exists in the database
        cursor.execute("SELECT * FROM users WHERE username=%s OR email=%s", (user.username, user.email))
        existing_user = cursor.fetchone()
        if existing_user:
            raise HTTPException(status_code=400, detail="Username or Email already exists")
        
        # If no existing user, hash the password and insert new user
        hashed_password = hash_password(user.password)
        cursor.execute("INSERT INTO users (username, email, password) VALUES (%s, %s, %s)", (user.username, user.email, hashed_password))
        conn.commit()
        conn.close()
        return {"message": "User registered successfully" }
    
    except Exception as e:
        return HTTPException(status_code=500, detail=str(e))

# User login endpoint
@app.post("/login")
def login_user(form_data: OAuth2PasswordRequestForm = Depends()):
    try:
        # Debugging: Checking incoming form data (username and password)
        print(f"Received login request with username: {form_data.username}")

        # Step 1: Establish a database connection
        conn = get_connection()
        if conn is None:
            raise HTTPException(status_code=500, detail="Database connection error")
        
        cursor = conn.cursor()

        # Step 2: Query the user from the database based on the username
        print(f"Querying database for user: {form_data.username}")
        cursor.execute("SELECT id, username, email, password FROM users WHERE username = %s", (form_data.username,))
        user = cursor.fetchone()
        conn.close()

        # Step 3: Check if the user exists in the database
        if not user:
            print(f"❌ User not found in database: {form_data.username}")
            raise HTTPException(status_code=400, detail="Invalid username or password")

        user_id, username, email, hashed_password = user
        print(f"✅ User found: {username}")

        # Step 4: Verify the provided password with the stored hash
        if not verify_password(form_data.password, hashed_password):
            print(f"❌ Password mismatch for user: {username}")
            raise HTTPException(status_code=400, detail="Invalid username or password")

        # Step 5: Generate JWT token for successful login
        access_token = create_access_token(
            data={"sub": username, "user_id": user_id},
            expires_delta=datetime.timedelta(hours=1)   # Token expires in 1 hour
        )
        
        print("✅ Login successful, JWT token generated.")

        # Step 6: Return the generated token
        return {"access_token": access_token, "token_type": "bearer"}

    except Exception as e:
        # Debugging: Logging the exception for easier debugging
        print(f"❌ Exception encountered: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")

    

# Function to verify JWT token
def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return {"user_id": payload.get("user_id"), "username": payload.get("sub")}
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")
    
# Example protected route
@app.get("/profile")
def get_profile(current_user: dict = Depends(get_current_user)):
    return {"message": "Welcome!", "user": current_user}


# Run the server with: uvicorn main:app --reload