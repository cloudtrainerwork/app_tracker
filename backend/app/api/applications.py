from fastapi import APIRouter, Depends, HTTPException
from typing import List
from ..models import job_application  # Import the Pydantic model
from ..services import supabase_client #Import Supabase here
router = APIRouter(
    prefix="/applications",
    tags=["applications"],
    dependencies=[],
    responses={404: {"description": "Not found"}},
)


@router.post("/", response_model=job_application.JobApplication)
async def create_application(application: job_application.JobApplication, user_id: str = Depends(verify_jwt_token)):
    """Create a new job application."""
    #Enforce user ID from token
    application.user_id = user_id
    data, error = supabase_client.supabase.table("job_applications").insert(application.dict()).execute()

    if error:
        raise HTTPException(status_code=500, detail=error)
    # Supabase returns a list of inserted records. Get the first one.
    return job_application.JobApplication(**data[1][0])# type: ignore

@router.get("/", response_model=List[job_application.JobApplication])
async def list_applications(user_id: str = Depends(verify_jwt_token)):
    """List all job applications for a user."""
    data, error = supabase_client.supabase.table("job_applications").select("*").eq("user_id", user_id).execute()

    if error:
        raise HTTPException(status_code=500, detail=error)

    applications = [job_application.JobApplication(**item) for item in data[1]] # type: ignore
    return applications


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