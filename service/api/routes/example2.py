from fastapi import APIRouter, HTTPException, status
from api.database import db, parse_obj_id
from api.models import ItemModel
from api.schemas import ItemCreate, ItemResponse
from bson import ObjectId

example2_router = APIRouter()


@example2_router.get("/{item_id}", response_model=ItemResponse)
async def get_item(item_id: str):
    if not ObjectId.is_valid(item_id):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid ID")
    item = await db["items"].find_one({"_id": ObjectId(item_id)})
    if not item:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item not found")
    return parse_obj_id(item)

@example2_router.put("/{item_id}", response_model=ItemResponse)
async def update_item(item_id: str, item: ItemCreate):
    if not ObjectId.is_valid(item_id):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid ID")
    result = await db["items"].update_one({"_id": ObjectId(item_id)}, {"$set": item.dict()})
    if result.modified_count == 0:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item not found")
    updated_item = await db["items"].find_one({"_id": ObjectId(item_id)})
    return parse_obj_id(updated_item)

@example2_router.delete("/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_item(item_id: str):
    if not ObjectId.is_valid(item_id):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid ID")
    result = await db["items"].delete_one({"_id": ObjectId(item_id)})
    if result.deleted_count == 0:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item not found")
