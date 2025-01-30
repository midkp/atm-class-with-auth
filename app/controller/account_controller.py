import jwt
from app.core.settings import SECRET_KEY
from passlib.context import CryptContext
from datetime import datetime, timedelta
from app.services.atm_service import ATMService
from sqlalchemy.ext.asyncio import AsyncSession
import logging

# Set up logging
logger = logging.getLogger("account_controller")
logger.setLevel(logging.INFO)

class AccountController:
    def __init__(self, db: AsyncSession):
        self.service = ATMService(db)
        self.pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

    async def create_account(self, username: str, pin: str, initial_deposit: float):
        hashed_pin = self.pwd_context.hash(pin)
        return await self.service.create_account(username, hashed_pin, initial_deposit)

    async def authenticate(self, username: str, pin: str):
        """Authenticate user and generate JWT token"""
        try:
            user = await self.service.get_user_by_username(username)
            if user and self.pwd_context.verify(pin, user.pin):
                # Create token for the user
                payload = {"username": username, "exp": datetime.utcnow() + timedelta(hours=1)}  # Expires in 1 hour
                token = jwt.encode(payload, SECRET_KEY, algorithm="HS256")
                return token
            return None  # Authentication failed
        except Exception as e:
            logger.error(f"Error during authentication: {e}")
            return None

    async def deposit(self, username: str, amount: float):
        try:
            return await self.service.deposit(username, amount)
        except Exception as e:
            logger.error(f"Error during deposit for user {username}: {e}")
            raise

    async def withdraw(self, username: str, amount: float):
        try:
            return await self.service.withdraw(username, amount)
        except Exception as e:
            logger.error(f"Error during withdrawal for user {username}: {e}")
            raise

    async def show_balance(self, username: str):
        try:
            return await self.service.show_balance(username)
        except Exception as e:
            logger.error(f"Error fetching balance for user {username}: {e}")
            raise

    async def show_transactions(self, username: str):
        try:
            return await self.service.show_transactions(username)
        except Exception as e:
            logger.error(f"Error fetching transactions for user {username}: {e}")
            raise

    async def logout(self, username: str):
        """Handle logout (invalidate session)"""
        # In a real-world scenario, you could invalidate the JWT or clear the session here
        try:
            logger.info(f"User {username} logged out successfully.")
            return True
        except Exception as e:
            logger.error(f"Error during logout for user {username}: {e}")
            return False
