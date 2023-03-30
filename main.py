from fastapi import FastAPI
from tortoise.contrib.fastapi import register_tortoise
from models import (User, Buisness, Product,
                    user_pydantic, user_pydanticIN, user_pydanticOut,
                    buisness_pydantic, buisness_pydanticIn,
                    product_pydantic, product_pydanticIn)
from authentication import get_hashed_password

# signals
from tortoise.signals import  post_save 
from typing import List, Optional, Type
from tortoise import BaseDBAsyncClient
from emails import EmailSchema, config_credentials, conf, send_email

# process signals here
@post_save(User)
async def create_business(
    sender: "Type[User]",
    instance: User,
    created: bool,
    using_db: "Optional[BaseDBAsyncClient]",
    update_fields: List[str]) -> None:
    
    if created:
        business_obj = await Buisness.create(
                business_name = instance.username, owner = instance)
        await buisness_pydantic.from_tortoise_orm(business_obj)
        # send email functionality
        await send_email([instance.email], instance)


app = FastAPI()


@app.post("/registration")
async def user_registration(user: user_pydanticIN):
    user_info = user.dict(exclude_unset = True)
    user_info["password"] = get_hashed_password(user_info["password"])
    user_obj = await User.create(**user_info)
    new_user = await user_pydanticOut.from_tortoise_orm(user_obj)
    return{
        "status": "OK",
        "data" : f"Hello {new_user.username} thanks for choosing our services. Please check your email inbox and click on the link to confirm your registration."
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

