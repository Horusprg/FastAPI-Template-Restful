from fastapi import APIRouter, HTTPException, status
from api.database import db, parse_obj_id
from api.models import ItemModel
from api.schemas import ItemCreate, ItemResponse
from bson import ObjectId

example1_router = APIRouter()


@example1_router.post(
    "/", response_model=ItemResponse, status_code=status.HTTP_201_CREATED
)
async def create_item(item: ItemCreate):
    item_data = item.dict()
    result = await db["items"].insert_one(item_data)
    item_data["_id"] = result.inserted_id
    return parse_obj_id(item_data)


@example1_router.get("/", response_model=list[ItemResponse])
async def list_items():
    items = await db["items"].find().to_list(100)
    return [parse_obj_id(item) for item in items]
