from typing import List
from typing import Optional

from fastapi import FastAPI
from fastapi import HTTPException
from pydantic import BaseModel

app = FastAPI()


class Item(BaseModel):
    id: Optional[int] = None
    name: str
    description: Optional[str] = None
    price: float
    tax: Optional[float] = None


@app.get("/")
def read_root():
    return {"Hello": "World"}


items_db = {}


@app.post("/items/", response_model=Item)
def create_item(item: Item):
    item.id = len(items_db) + 1  # Simple ID generation
    items_db[item.id] = item
    return item


@app.get("/items/", response_model=List[Item])
def read_items():
    return list(items_db.values())


@app.get("/items/{item_id}", response_model=Item)
def read_item(item_id: int):
    if item_id not in items_db:
        raise HTTPException(status_code=404, detail="Item not found")
    return items_db[item_id]


@app.put("/items/{item_id}", response_model=Item)
def update_item(item_id: int, item: Item):
    if item_id not in items_db:
        raise HTTPException(status_code=404, detail="Item not found")
    item.id = item_id
    items_db[item_id] = item
    return item


@app.delete("/items/{item_id}", response_model=Item)
def delete_item(item_id: int):
    if item_id not in items_db:
        raise HTTPException(status_code=404, detail="Item not found")
    return items_db.pop(item_id)
