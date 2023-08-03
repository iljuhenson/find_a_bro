import typing

import strawberry

@strawberry.input
class UserType:
    id: int    
    email: str
    password: str
    first_name: str
    last_name: str
    description: str
    profile_picture_path: str
    is_active: bool
