from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import mysql.connector
import bcrypt
import os
from dotenv import load_dotenv
import logging

# Load environment variables
load_dotenv()

# Set up logging
logging.basicConfig(level=logging.DEBUG)

# FastAPI app initialization
app = FastAPI()

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Pydantic model for login
class LoginRequest(BaseModel):
    username: str
    password: str

# Database connection
def create_connection():
    try:
        connection = mysql.connector.connect(
            host=os.getenv("RDS_HOST"),
            user=os.getenv("RDS_USER"),
            password=os.getenv("RDS_PASSWORD"),
            database=os.getenv("RDS_DB"),
        )
        return connection
    except mysql.connector.Error as e:
        logging.error(f"Database connection error: {e}")
        raise HTTPException(status_code=500, detail="Database connection error")

# Root endpoint
@app.get("/")
def root():
    return {"message": "Welcome to the F1 Pit Stop API"}

# Favicon route to prevent 404
@app.get("/favicon.ico")
def favicon():
    return {"message": "No favicon available"}

# Login endpoint
@app.post("/login/")
def login_user(request: LoginRequest):
    try:
        connection = create_connection()
        cursor = connection.cursor(dictionary=True)
        query = "SELECT * FROM login WHERE username = %s"
        cursor.execute(query, (request.username,))
        user = cursor.fetchone()
        cursor.close()
        connection.close()

        if not user:
            raise HTTPException(status_code=401, detail="Invalid username or password")

        # Log for debugging
        logging.debug(f"Stored hash: {user['password']}")
        logging.debug(f"Password entered: {request.password}")

        if bcrypt.checkpw(request.password.encode('utf-8'), user['password'].encode('utf-8')):
            return {
                "id": user["id"],
                "fname": user["fname"],
                "lname": user["lname"],
                "user_type": user["user_type"],
            }
        else:
            raise HTTPException(status_code=401, detail="Invalid username or password")
    except Exception as e:
        logging.error(f"Error in login_user: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")
