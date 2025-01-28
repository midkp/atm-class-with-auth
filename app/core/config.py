from fastapi import FastAPI
from pydantic import BaseModel

class CreateAccountRequest(BaseModel):
    username: str
    pin: str
    initial_deposit: float

class DepositWithdrawRequest(BaseModel):
    username: str
    amount: float

class BalanceTransactions(BaseModel):
    username: str