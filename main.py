from fastapi import FastAPI
from tortoise.contrib.fastapi import register_tortoise
from models import (User, Buisness, Product,
                    user_pydantic, user_pydanticIN, user_pydanticOut,
                    buisness_pydantic, buisness_pydanticIn,
                    product_pydantic, product_pydanticIn)
from authentication import get_hashed_password
app = FastAPI()


@app.post("/registration")
async def user_registration(user: user_pydanticIN):
    user_info = user.dict(exclude_unset = True)
    user_info["password"] = get_hashed_password(user_info["password"])
    user_obj = await User.create(**user_info)
    new_user = await user_pydanticOut.from_tortoise_orm(user_obj)
    return{
        "status": "OK",
        "data" : f"Hello{new_user.username} thanks for choosing our services. Please check your email inbox and click on the link to confirm your registration."
    }
    
    

@app.get("/")
def index():
    return {"Message" : "Hello World!"}

register_tortoise(
    app,
    db_url="sqlite://db.sqlite3",
    modules={"models": ["models"]},
    generate_schemas=True,
    add_exception_handlers=True
)

