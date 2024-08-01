from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional, List

app = FastAPI()

# Define a Pydantic model for the request body
class Item(BaseModel):
    name: str
    description: Optional[str] = None
    price: float
    tax: Optional[float] = None

# Static data for demonstration
static_items = [
    Item(name="Item1", description="Description for Item1", price=10.99, tax=1.5),
    Item(name="Item2", description="Description for Item2", price=20.49, tax=2.0),
    Item(name="Item3", description="Description for Item3", price=5.99, tax=0.5),
]

# GET endpoint to fetch all items
@app.get("/items/", response_model=List[Item])
async def get_items():
    return static_items

# GET endpoint to fetch an item by name
@app.get("/items/{item_name}", response_model=Item)
async def get_item(item_name: str):
    for item in static_items:
        if item.name == item_name:
            return item
    raise HTTPException(status_code=404, detail="Item not found")

# POST endpoint to add a new item (to static data for demo)
@app.post("/items/", response_model=Item)
async def create_item(item: Item):
    static_items.append(item)
    return item

# POST endpoint to update an existing item (in static data for demo)
@app.post("/items/{item_name}/update", response_model=Item)
async def update_item(item_name: str, item: Item):
    for index, existing_item in enumerate(static_items):
        if existing_item.name == item_name:
            static_items[index] = item
            return item
    raise HTTPException(status_code=404, detail="Item not found")

# Run the application
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)