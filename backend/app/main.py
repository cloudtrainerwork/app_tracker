import os
from typing import Optional

from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from supabase import create_client, Client

# API keys and database URL (Supabase)
SUPABASE_URL = os.environ.get("SUPABASE_URL")
SUPABASE_KEY = os.environ.get("SUPABASE_KEY")

# Initialize Supabase client
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# FastAPI app
app = FastAPI()

# CORS configuration (adjust as needed for security)
origins = ["*"]  # Allow all origins (for development only!)

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Data models
class JobApplication(BaseModel):
    user_id: str  # Link to the Supabase Auth user ID
    company_name: str
    job_title: str
    application_date: str  # Use ISO 8601 format (YYYY-MM-DD)
    status: str = "Applied"  # Default status
    source: Optional[str] = None
    job_number: Optional[str] = None  # Add Job Number

class EmailInteraction(BaseModel):
    application_id: str # Link to the JobApplication ID
    user_id: str  # Link to the Supabase Auth user ID
    gmail_message_id: str
    interaction_date: str  # Use ISO 8601 format (YYYY-MM-DD)
    sender: str
    subject: str
    snippet: str  # Short extract of the email body
    interaction_type: str  # Application Confirmation, Interview Invite, Rejection, etc.


# Dependency to verify JWT token (example - integrate with Supabase Auth)
async def verify_jwt_token(token: str):
    """Verify JWT with Supabase Auth.  Returns user_id on success, raises
    HTTPException on failure.  This is a placeholder.  Implement robust
    validation per Supabase documentation.
    """
    #IMPLEMENT TOKEN VALIDATION HERE based on your Supabase setup
    #and JWT structure. This is a placeholder example.
    # You might use libraries like `jose` to verify the signature.

    #  For now, we'll just assume the first three characters is the user_id
    if len(token) < 3:
        raise HTTPException(status_code=401, detail="Invalid token")
    return token[0:3]


# API endpoints
@app.post("/applications/", response_model=JobApplication)
async def create_application(application: JobApplication, user_id: str = Depends(verify_jwt_token)):
    """Create a new job application."""
    application.user_id = user_id  # Enforce user ID from token
    data, error = supabase.table("job_applications").insert(application.dict()).execute()

    if error:
        raise HTTPException(status_code=500, detail=error)

    # Supabase returns a list of inserted records. Get the first one.
    return JobApplication(**data[1][0]) # type: ignore


@app.get("/applications/", response_model=list[JobApplication])
async def list_applications(user_id: str = Depends(verify_jwt_token)):
    """List all job applications for a user."""
    data, error = supabase.table("job_applications").select("*").eq("user_id", user_id).execute()

    if error:
        raise HTTPException(status_code=500, detail=error)

    applications = [JobApplication(**item) for item in data[1]]  # type: ignore
    return applications

@app.get("/applications/{application_id}", response_model=JobApplication)
async def get_application(application_id: str, user_id: str = Depends(verify_jwt_token)):
     """Get application by id."""

     data, error = supabase.table("job_applications").select("*").eq("id", application_id).eq("user_id", user_id).execute()

     if error:
        raise HTTPException(status_code=500, detail=error)

     if not data[1]:
        raise HTTPException(status_code=404, detail="Application not found")

     return JobApplication(**data[1][0]) # type: ignore


@app.post("/interactions/", response_model=EmailInteraction)
async def create_interaction(interaction: EmailInteraction, user_id: str = Depends(verify_jwt_token)):
    """Create a new email interaction."""
    interaction.user_id = user_id #Enforce user ID from token
    data, error = supabase.table("email_interactions").insert(interaction.dict()).execute()

    if error:
        raise HTTPException(status_code=500, detail=error)

    return EmailInteraction(**data[1][0]) # type: ignore

@app.get("/interactions/{application_id}", response_model=list[EmailInteraction])
async def list_interactions(application_id: str, user_id: str = Depends(verify_jwt_token)):
    """List all email interactions for a given application."""
    data, error = supabase.table("email_interactions").select("*").eq("application_id", application_id).eq("user_id", user_id).execute() #Ensure interactions belong to user

    if error:
        raise HTTPException(status_code=500, detail=error)

    interactions = [EmailInteraction(**item) for item in data[1]]  # type: ignore
    return interactions