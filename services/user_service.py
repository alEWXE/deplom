# from db.mongo import get_user_collection
# from schemas.user import UserCreate, UserLogin
# from fastapi import Depends
# from passlib.context import CryptContext

# pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# class UniqueViolation(Exception): pass
# class UserDoesNotExist(Exception): pass

# class UserService:
#     def __init__(self, users = Depends(get_user_collection)):
#         self.users = users

#     def create_user(self, data: UserCreate):
#         if self.users.find_one({"email": data.email}):
#             raise UniqueViolation("Email already taken")
#         hashed = pwd_context.hash(data.password)
#         user = {"email": data.email, "password": hashed}
#         self.users.insert_one(user)
#         return user

#     def get_user(self, data: UserLogin):
#         user = self.users.find_one({"email": data.email})
#         if not user or not pwd_context.verify(data.password, user["password"]):
#             raise UserDoesNotExist()
#         return user
