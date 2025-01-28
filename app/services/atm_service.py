from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.services.models import User, Transaction
from fastapi import HTTPException
import logging

# Get the logger instance from the logging_config.py
from app.core.logging_config import logger

class ATMService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create_account(self, username, pin, initial_deposit):
        try:
            # Querying asynchronously
            result = await self.db.execute(select(User).filter(User.username == username))
            existing_user = result.scalars().first()
            if existing_user:
                raise HTTPException(status_code=400, detail="Username already exists")

            new_user = User(username=username, pin=pin, balance=initial_deposit)
            self.db.add(new_user)
            await self.db.commit()  # Use await with commit
            await self.db.refresh(new_user)  # Use await with refresh
            return {"message": f"Account created successfully for {username}"}
        except Exception as e:
            logger.error(f"Error in creating account for {username}: {str(e)}")
            raise HTTPException(status_code=500, detail="Internal Server Error")

    async def deposit(self, username, amount):
        try:
            # Querying asynchronously
            result = await self.db.execute(select(User).filter(User.username == username))
            user = result.scalars().first()
            if not user:
                raise HTTPException(status_code=404, detail="User not found")

            user.balance += amount
            transaction = Transaction(user_id=user.id, type="deposit", amount=amount)
            self.db.add(transaction)
            await self.db.commit()  # Use await with commit
            return {"message": f"Deposited ${amount:.2f}. New balance: ${user.balance:.2f}"}
        except Exception as e:
            logger.error(f"Error in depositing amount for {username}: {str(e)}")
            raise HTTPException(status_code=500, detail="Internal Server Error")

    async def withdraw(self, username, amount):
        try:
            # Querying asynchronously
            result = await self.db.execute(select(User).filter(User.username == username))
            user = result.scalars().first()
            if not user:
                raise HTTPException(status_code=404, detail="User not found")

            if user.balance < amount:
                raise HTTPException(status_code=400, detail="Insufficient balance")

            user.balance -= amount
            transaction = Transaction(user_id=user.id, type="withdrawal", amount=amount)
            self.db.add(transaction)
            await self.db.commit()  # Use await with commit
            return {"message": f"Withdrew ${amount:.2f}. New balance: ${user.balance:.2f}"}
        except Exception as e:
            logger.error(f"Error in withdrawing amount for {username}: {str(e)}")
            raise HTTPException(status_code=500, detail="Internal Server Error")

    async def show_balance(self, username: str):
        try:
            # Use 'select' to create the query
            stmt = select(User).filter(User.username == username)

            # Execute the query asynchronously and fetch the result
            result = await self.db.execute(stmt)

            # Fetch the results as a list of rows
            user = result.scalars().first()  # Use scalars().first() for async result fetching

            if not user:
                raise HTTPException(status_code=404, detail="User not found")

            return {"balance": user.balance}
        except Exception as e:
            logger.error(f"Error in fetching balance for {username}: {str(e)}")
            raise HTTPException(status_code=500, detail="Internal Server Error")

    async def show_transactions(self, username):
        try:
            # Querying asynchronously
            result = await self.db.execute(select(User).filter(User.username == username))
            user = result.scalars().first()
            if not user:
                raise HTTPException(status_code=404, detail="User not found")

            result = await self.db.execute(select(Transaction).filter(Transaction.user_id == user.id))
            transactions = result.scalars().all()  # Fetch all the transactions asynchronously

            return [{"type": tx.type, "amount": tx.amount, "date": tx.date} for tx in transactions]
        except Exception as e:
            logger.error(f"Error in fetching transactions for {username}: {str(e)}")
            raise HTTPException(status_code=500, detail="Internal Server Error")
