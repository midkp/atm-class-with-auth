from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.dependencies.database import get_db
from app.controller.account_controller import AccountController
<<<<<<< HEAD
from app.core.config import CreateAccountRequest, DepositWithdrawRequest, BalanceTransactions
import logging
=======
from app.core.config import CreateAccountRequest, DepositWithdrawRequest
from app.schemas import LoginRequest
>>>>>>> feature/atm-auth-midhun-20250128

router = APIRouter()

# Account creation
@router.post("/create-account", tags=["Account Management"], name="Create Account")
async def create_account(request: CreateAccountRequest, db: AsyncSession = Depends(get_db)):
    controller = AccountController(db)
    return await controller.create_account(request.username, request.pin, request.initial_deposit)

# Login - authenticate the user
@router.post("/login", tags=["Authentication"], name="Login")
async def login(request: LoginRequest, db: AsyncSession = Depends(get_db)): 
    controller = AccountController(db)
    # Authenticate user with username and pin
    token = await controller.authenticate(request.username, request.pin)
    if token:
        return {"message": "Login successful", "token": token}
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

<<<<<<< HEAD
# Check balance - renamed from /balance to /check-balance
import logging

# Configure logging
logger = logging.getLogger("uvicorn")

=======
# Check balance
>>>>>>> feature/atm-auth-midhun-20250128
@router.get("/check-balance", tags=["Account"])
async def check_balance(username: str, db: AsyncSession = Depends(get_db)):
    logger.debug(f"Received request for check balance with username: {username}")
    controller = AccountController(db)
<<<<<<< HEAD
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
=======
    balance = await controller.show_balance(username)
    if balance is None:
        raise HTTPException(status_code=404, detail="User not found")
    return {"username": username, "balance": balance}
>>>>>>> feature/atm-auth-midhun-20250128
