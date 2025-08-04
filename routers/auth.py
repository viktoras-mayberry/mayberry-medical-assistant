from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from auth import (
    authenticate_user, 
    create_access_token, 
    get_password_hash, 
    get_current_active_user
)
from database import get_db
from models import User
from schemas import (
    UserCreate, UserResponse, UserLogin, Token, APIResponse, 
    UserProfileCreate, UserProfileUpdate, UserProfileResponse
)
from models import UserProfile
import json

router = APIRouter()

@router.post("/register", response_model=UserResponse)
def register_user(user: UserCreate, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.email == user.email).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    hashed_password = get_password_hash(user.password)
    db_user = User(email=user.email, hashed_password=hashed_password, full_name=user.full_name)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

@router.post("/login", response_model=Token)
def login_for_access_token(form_data: UserLogin, db: Session = Depends(get_db)):
    user = authenticate_user(db, email=form_data.email, password=form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token = create_access_token(
        data={"sub": user.email}
    )
    return {"access_token": access_token, "token_type": "bearer"}

@router.get("/me", response_model=UserResponse)
def read_users_me(current_user: User = Depends(get_current_active_user)):
    return current_user

@router.get("/profile", response_model=UserProfileResponse)
def get_user_profile(current_user: User = Depends(get_current_active_user), db: Session = Depends(get_db)):
    """Get current user's profile"""
    profile = db.query(UserProfile).filter(UserProfile.user_id == current_user.id).first()
    if not profile:
        # Create default profile if it doesn't exist
        profile = UserProfile(user_id=current_user.id)
        db.add(profile)
        db.commit()
        db.refresh(profile)
    return profile

@router.post("/profile", response_model=UserProfileResponse)
def create_user_profile(
    profile_data: UserProfileCreate, 
    current_user: User = Depends(get_current_active_user), 
    db: Session = Depends(get_db)
):
    """Create or update user profile"""
    existing_profile = db.query(UserProfile).filter(UserProfile.user_id == current_user.id).first()
    if existing_profile:
        raise HTTPException(status_code=400, detail="Profile already exists. Use PUT to update.")
    
    # Convert lists to JSON strings for storage
    profile_dict = profile_data.dict()
    for field in ['allergies', 'chronic_conditions', 'current_medications']:
        if profile_dict.get(field):
            profile_dict[field] = json.dumps(profile_dict[field])
    
    profile = UserProfile(user_id=current_user.id, **profile_dict)
    db.add(profile)
    db.commit()
    db.refresh(profile)
    return profile

@router.put("/profile", response_model=UserProfileResponse)
def update_user_profile(
    profile_data: UserProfileUpdate, 
    current_user: User = Depends(get_current_active_user), 
    db: Session = Depends(get_db)
):
    """Update user profile"""
    profile = db.query(UserProfile).filter(UserProfile.user_id == current_user.id).first()
    if not profile:
        # Create profile if it doesn't exist
        profile = UserProfile(user_id=current_user.id)
        db.add(profile)
    
    # Update only provided fields
    update_data = profile_data.dict(exclude_unset=True)
    for field in ['allergies', 'chronic_conditions', 'current_medications']:
        if field in update_data and update_data[field] is not None:
            update_data[field] = json.dumps(update_data[field])
    
    for field, value in update_data.items():
        setattr(profile, field, value)
    
    db.commit()
    db.refresh(profile)
    return profile

@router.delete("/profile", response_model=APIResponse)
def delete_user_profile(
    current_user: User = Depends(get_current_active_user), 
    db: Session = Depends(get_db)
):
    """Delete user profile"""
    profile = db.query(UserProfile).filter(UserProfile.user_id == current_user.id).first()
    if not profile:
        raise HTTPException(status_code=404, detail="Profile not found")
    
    db.delete(profile)
    db.commit()
    return {"success": True, "message": "Profile deleted successfully"}
