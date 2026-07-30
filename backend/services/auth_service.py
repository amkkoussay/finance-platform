from models import db
from models.user import User
from services.token_service import generate_token
from services.validation import ValidationError, validate_email, validate_password


class AuthService:
    @staticmethod
    def register(email, username, password, confirm_password):
        validate_email(email)
        validate_password(password, confirm_password)

        if not username or not username.strip():
            raise ValidationError("Username is required")

        if User.query.filter_by(email=email).first():
            raise ValidationError("Email is already registered")

        if User.query.filter_by(username=username).first():
            raise ValidationError("Username is already taken")

        user = User(email=email, username=username)
        user.set_password(password)

        db.session.add(user)
        db.session.commit()

        token = generate_token(user.id)
        return {
            "user_id": user.id,
            "email": user.email,
            "username": user.username,
            "token": token,
        }

    @staticmethod
    def login(email, password):
        if not email or not password:
            raise ValidationError("Email and password are required")

        user = User.query.filter_by(email=email).first()
        if not user or not user.check_password(password):
            raise ValidationError("Invalid email or password")

        token = generate_token(user.id)
        return {
            "user_id": user.id,
            "username": user.username,
            "email": user.email,
            "token": token,
        }
