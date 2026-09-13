from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.models import User
from app.schemas.auth import UserCreate, UserLogin, UserOut, Token, UserUpdate
from app.auth.security import get_password_hash, verify_password, create_access_token
from app.auth.deps import get_current_user

router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post("/register", response_model=Token, status_code=status.HTTP_201_CREATED)
def register(user_in: UserCreate, db: Session = Depends(get_db)):
    """Register a new user account with validated credentials."""
    existing_user = db.query(User).filter(User.email == user_in.email.lower()).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="An account with this email address already exists. Please log in.",
        )

    hashed_pw = get_password_hash(user_in.password)
    new_user = User(
        name=user_in.name.strip(),
        email=user_in.email.lower().strip(),
        password_hash=hashed_pw,
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    token = create_access_token({"sub": str(new_user.id)})
    return Token(access_token=token, token_type="bearer", user=UserOut.model_validate(new_user))


@router.post("/login", response_model=Token)
def login(user_in: UserLogin, db: Session = Depends(get_db)):
    """Authenticate existing user credentials and return a signed JWT access token."""
    user = db.query(User).filter(User.email == user_in.email.lower().strip()).first()
    if not user or not verify_password(user_in.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password. Please check your credentials.",
        )

    token = create_access_token({"sub": str(user.id)})
    return Token(access_token=token, token_type="bearer", user=UserOut.model_validate(user))


@router.get("/me", response_model=UserOut)
def get_me(current_user: User = Depends(get_current_user)):
    """Return the currently authenticated user's profile details."""
    return current_user


@router.put("/profile", response_model=UserOut)
def update_profile(
    update_data: UserUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Update profile name and optionally change password with current password verification."""
    if update_data.name:
        current_user.name = update_data.name.strip()

    if update_data.new_password:
        if not update_data.current_password or not verify_password(
            update_data.current_password, current_user.password_hash
        ):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Current password is incorrect.",
            )
        if len(update_data.new_password) < 6:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="New password must be at least 6 characters long.",
            )
        current_user.password_hash = get_password_hash(update_data.new_password)

    db.commit()
    db.refresh(current_user)
    return current_user


@router.delete("/account", status_code=status.HTTP_200_OK)
def delete_account(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Delete current user account and all associated resumes and analyses."""
    db.delete(current_user)
    db.commit()
    return {"message": "Account successfully deleted."}
