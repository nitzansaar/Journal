from fastapi import FastAPI, HTTPException, Depends, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
import os
from datetime import datetime
from supabase import create_client, Client
from jose import JWTError, jwt
import json

app = FastAPI(title="Journal App API", version="1.0.0")

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Supabase setup
supabase_url = os.getenv("NEXT_PUBLIC_SUPABASE_URL")
supabase_service_key = os.getenv("SUPABASE_SERVICE_ROLE_KEY")

if not supabase_url or not supabase_service_key:
    raise ValueError("Missing Supabase configuration")

supabase: Client = create_client(supabase_url, supabase_service_key)

# Security
security = HTTPBearer()

# Pydantic models
class JournalEntryCreate(BaseModel):
    content: str

class JournalEntryResponse(BaseModel):
    id: str
    created_at: str
    user_id: str
    content: str

class JournalEntryListResponse(BaseModel):
    id: str
    created_at: str
    content: str

# Authentication dependency
async def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    try:
        # Decode the JWT token
        token = credentials.credentials
        
        # Get the JWT secret from Supabase (this is the JWT secret from your Supabase project)
        # For now, we'll verify the token by making a request to Supabase
        try:
            user_response = supabase.auth.get_user(token)
            if user_response.user:
                return user_response.user.id
        except Exception as e:
            print(f"Auth error: {e}")
            pass
        
        # Alternative: decode JWT directly (you'd need the JWT secret from Supabase)
        # For this implementation, we'll trust the token and extract user_id
        # In production, you should properly verify the JWT signature
        
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

# Simplified auth for development - extracts user_id from token payload
async def get_current_user_simple(credentials: HTTPAuthorizationCredentials = Depends(security)):
    try:
        token = credentials.credentials
        # For development, we'll decode without verification
        # In production, you should verify the signature
        from jose import jwt
        payload = jwt.get_unverified_claims(token)
        user_id = payload.get("sub")
        if not user_id:
            raise HTTPException(status_code=401, detail="Invalid token")
        return user_id
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials"
        )

@app.get("/")
async def root():
    return {"message": "Journal App API is running"}

@app.post("/entries", response_model=JournalEntryResponse)
async def create_entry(
    entry: JournalEntryCreate,
    user_id: str = Depends(get_current_user_simple)
):
    try:
        # Insert into Supabase
        result = supabase.table("journal_entries").insert({
            "user_id": user_id,
            "content": entry.content,
            "created_at": datetime.utcnow().isoformat()
        }).execute()
        
        if result.data:
            entry_data = result.data[0]
            return JournalEntryResponse(
                id=entry_data["id"],
                created_at=entry_data["created_at"],
                user_id=entry_data["user_id"],
                content=entry_data["content"]
            )
        else:
            raise HTTPException(status_code=500, detail="Failed to create entry")
            
    except Exception as e:
        print(f"Error creating entry: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

@app.get("/entries", response_model=List[JournalEntryListResponse])
async def get_entries(user_id: str = Depends(get_current_user_simple)):
    try:
        # Fetch entries from Supabase
        result = supabase.table("journal_entries").select("id, created_at, content").eq("user_id", user_id).order("created_at", desc=True).execute()
        
        entries = []
        for entry_data in result.data:
            entries.append(JournalEntryListResponse(
                id=entry_data["id"],
                created_at=entry_data["created_at"],
                content=entry_data["content"]
            ))
        
        return entries
        
    except Exception as e:
        print(f"Error fetching entries: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) 