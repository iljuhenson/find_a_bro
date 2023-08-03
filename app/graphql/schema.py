import typing
import strawberry


@strawberry.type
class User:
    id: int    
    email: str
    password: str
    first_name: str
    last_name: str
    description: str
    profile_picture_path: str
    is_active: bool
