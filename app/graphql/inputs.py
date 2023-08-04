from typing import Optional
import strawberry

@strawberry.input
class UserSignUpInput:    
    email: str
    password: str
    first_name: str
    last_name: str