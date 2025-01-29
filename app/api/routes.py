from fastapi import APIRouter, Depends, Query, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.dependencies.database import get_db
from app.controller.account_controller import AccountController
from app.core.config import CreateAccountRequest, DepositWithdrawRequest, BalanceTransactions
import logging

router = APIRouter()

# Account creation
@router.post("/create-account", tags=["Account Management"], name="Create Account")
async def create_account(request: CreateAccountRequest, db: AsyncSession = Depends(get_db)):
    controller = AccountController(db)
    return await controller.create_account(request.username, request.pin, request.initial_deposit)

# Login - authenticate the user
@router.post("/login", tags=["Authentication"], name="Login")
async def login(username: str, password: str, db: AsyncSession = Depends(get_db)):
    controller = AccountController(db)
    
    # Here, replace with proper password hashing and validation
    if await controller.authenticate(username, password):  # Assuming you have an `authenticate` method
        return {"message": "Login successful"}
    else:
        raise HTTPException(status_code=401, detail="Invalid credentials")

# Logout - invalidate the session (for now just a placeholder)
@router.post("/logout", tags=["Authentication"], name="Logout")
async def logout():
    return {"message": "Logout successful"}

# Deposit
@router.post("/deposit", tags=["Account Management"], name="Deposit Money")
async def deposit(request: DepositWithdrawRequest, db: AsyncSession = Depends(get_db)):
    controller = AccountController(db)
    return await controller.deposit(request.username, request.amount)

# Withdraw
@router.post("/withdraw", tags=["Account Management"], name="Withdraw Money")
async def withdraw(request: DepositWithdrawRequest, db: AsyncSession = Depends(get_db)):
    controller = AccountController(db)
    return await controller.withdraw(request.username, request.amount)

# Check balance - renamed from /balance to /check-balance
import logging

# Configure logging
logger = logging.getLogger("uvicorn")

@router.get("/check-balance", tags=["Account"])
async def check_balance(username: str, db: AsyncSession = Depends(get_db)):
    logger.debug(f"Received request for check balance with username: {username}")
    controller = AccountController(db)
    try:
        balance = await controller.show_balance(username)
        if balance is None:
            raise HTTPException(status_code=404, detail="User not found")
        return balance
    except HTTPException as e:
        raise e
    except Exception as e:
        logger.error(f"Error fetching balance: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")

# Show transactions - renamed from /transactions to /show-transactions
@router.get("/show-transactions", tags=["Account Information"], name="View Transactions")
async def show_transactions(username: str = Query(..., description="The username for which to fetch transactions"), db: AsyncSession = Depends(get_db)):
    controller = AccountController(db)
    return await controller.show_transactions(username)
