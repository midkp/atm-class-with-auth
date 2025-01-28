from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.models import User  # Ensure the correct import path for the User model

class UserService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create_account(self, user_id, initial_deposit):
        # Example implementation for creating an account (may vary based on your schema)
        user = User(id=user_id, balance=initial_deposit)
        self.db.add(user)
        await self.db.commit()
        print(f"Account created for {user_id} with balance {initial_deposit}")

    async def deposit(self, user_id, amount):
        # Deposit logic
        user = await self.db.execute(select(User).where(User.id == user_id))
        user = user.scalars().first()
        if user:
            user.balance += amount
            await self.db.commit()
            print(f"Deposited {amount} for user {user_id}")
        else:
            raise ValueError("User not found")

    async def withdraw(self, user_id, amount):
        # Withdraw logic
        user = await self.db.execute(select(User).where(User.id == user_id))
        user = user.scalars().first()
        if user and user.balance >= amount:
            user.balance -= amount
            await self.db.commit()
            print(f"Withdrew {amount} for user {user_id}")
        else:
            raise ValueError("Insufficient funds or user not found")

    async def show_balance(self, user_id):
        # Fetch balance from DB asynchronously
        result = await self.db.execute(select(User).where(User.id == user_id))
        user = result.scalars().first()  # This extracts the user object from the result
        if user:
            return user.balance
        else:
            raise ValueError("User not found")
        
    async def show_transactions(self, user_id):
        # Example for fetching transactions, you need to implement this as per your schema
        pass
