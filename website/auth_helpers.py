from dataclasses import dataclass, field
from .models import User

@dataclass(frozen=True)
class ValidateLogin():  
    is_valid: bool = field(default=False)
    flash_message: str = field(default="") 


def is_valid_user(user: User | None, username: str, email: str, password: str, password_confirm: str) -> ValidateLogin:

    if user:
        return ValidateLogin(is_valid=False, flash_message="User already exists")
    
    if len(email) < 6:
        return ValidateLogin(is_valid=False, flash_message="Email length must be greater than 6 characters")
    
    if len(username) < 6:
        return ValidateLogin(is_valid=False, flash_message="Username length must be grater than 6 characters")
    
    if len(password) < 8:
        return ValidateLogin(is_valid=False, flash_message="Password length must be grater then 8 characters")

    # if password != password_confirm:
    #     return ValidateLogin(is_valid=False, flash_message="Passwords are not matching")    

    return ValidateLogin(is_valid=True, flash_message="All good")
