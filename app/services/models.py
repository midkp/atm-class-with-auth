from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from passlib.context import CryptContext  # Add passlib for hashing
from app.dependencies.database import Base  # Import Base from database

# Password hashing context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# User model
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    pin = Column(String, nullable=False)  # This will store the hashed pin
    balance = Column(Float, default=0.0)
    api_key = Column(String, nullable=True)

    transactions = relationship("Transaction", back_populates="user")

    # Hash the pin
    def set_pin(self, raw_pin: str):
        self.pin = pwd_context.hash(raw_pin)

    # Verify the hashed pin
    def verify_pin(self, raw_pin: str):
        return pwd_context.verify(raw_pin, self.pin)

# Transaction model
class Transaction(Base):
    __tablename__ = "transactions"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    type = Column(String, nullable=False)  # 'deposit' or 'withdrawal'
    amount = Column(Float, nullable=False)
    date = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="transactions")
