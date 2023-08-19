from fastapi import APIRouter
from app.functions.optimisation import Createschedule
router=APIRouter(prefix="/api/scheduling",
              responses={404:{"discription": "not found"}})

@router.post("/")
async def scheduling(value:dict):
    result= Createschedule(value)

    return result