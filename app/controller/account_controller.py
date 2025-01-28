from app.services.atm_service import ATMService
from sqlalchemy.ext.asyncio import AsyncSession
from app.services.models import User  # Import the User model
from passlib.context import CryptContext  # Import passlib for hashing and verification
from sqlalchemy.sql import text  # Import text to handle raw SQL queries
import logging

# Set up logging
logger = logging.getLogger("account_controller")
logger.setLevel(logging.INFO)

class AccountController:
    def __init__(self, db: AsyncSession):  # Accept AsyncSession
        self.service = ATMService(db)
        self.pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

    async def create_account(self, username: str, pin: str, initial_deposit: float):
        # Hash the pin before storing it in the database
        hashed_pin = self.pwd_context.hash(pin)
        # Use the service to create an account with the hashed pin
        return await self.service.create_account(username, hashed_pin, initial_deposit)

    async def authenticate(self, username: str, pin: str) -> bool:
        # Query the database for the user using a raw SQL query
        try:
            async with self.service.db as session:
                result = await session.execute(
                    text("SELECT * FROM users WHERE username = :username"), {"username": username}
                )
                user = result.fetchone()  # Safely fetch one record from the query

            if user:
                # Access the 'pin' field from the query result
                stored_pin = user['pin'] if isinstance(user, dict) else getattr(user, 'pin', None)

                if stored_pin and isinstance(stored_pin, str):  # Ensure stored_pin is a non-empty string
                    try:
                        # Verify the pin against the hashed value
                        if self.pwd_context.verify(pin, stored_pin):
                            return True
                    except Exception as e:
                        logger.error(f"Error during pin verification: {e}")
                        return False
            return False  # Return False if no user is found or pin verification fails

        except Exception as e:
            logger.error(f"Error during authentication: {e}")
            return False

    async def deposit(self, username: str, amount: float):
        # Use the service to handle deposit logic
        try:
            return await self.service.deposit(username, amount)
        except Exception as e:
            logger.error(f"Error during deposit for user {username}: {e}")
            raise

    async def withdraw(self, username: str, amount: float):
        # Use the service to handle withdrawal logic
        try:
            return await self.service.withdraw(username, amount)
        except Exception as e:
            logger.error(f"Error during withdrawal for user {username}: {e}")
            raise

    async def show_balance(self, username: str):
        # Use the service to fetch the user's balance
        try:
            return await self.service.show_balance(username)
        except Exception as e:
            logger.error(f"Error fetching balance for user {username}: {e}")
            raise

    async def show_transactions(self, username: str):
        # Use the service to fetch transaction history
        try:
            return await self.service.show_transactions(username)
        except Exception as e:
            logger.error(f"Error fetching transactions for user {username}: {e}")
            raise
