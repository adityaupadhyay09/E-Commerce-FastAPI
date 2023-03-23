from tortoise import Model, fields
from pydantic import BaseModel
from datetime import datetime
import pytz
from tortoise.contrib.pydantic import pydantic_model_creator


class User(Model):
    id = fields.IntField(pk = True, index = True)
    username = fields.CharField(max_length = 50, null = False, unique = True)
    email = fields.EmailField(unique = True, null = False)
    password = password = fields.PasswordField(null = False)
    is_verified = fields.BooleanField(default=False)
    join_date = fields.DatetimeField(auto_now_add=True, tzinfo=pytz.timezone('Asia/Kolkata'))
    
    
class Buisness(Model):
    id = fields.IntField(pk = True, index = True)
    buisness_name = fields.CharField(max_length = 250, null = False, unique = True)
    city = fields.CharField(max_length = 100, null = False, default = "Unspecified")
    region = fields.CharField(max_length = 100, null = False, default = "Unspecified")
    buisness_description = fields.TextField(null = False)
    logo_name = fields.CharField(max_length = 255, null = False)
    logo_image = fields.BinaryField(max_length=1000000, null = False, default = "default.jpg")
    owner = fields.ForeignKeyField("models.User", related_name="buisness")
    
    
class Product(Model):
    id = fields.IntField(pk = True, index = True)
    name = fields.CharField(max_length = 100, null = False, index = True)
    category = fields.CharField(max_length=100, index=True)
    original_price = fields.DecimalField(max_digits=12, decimal_places=2)
    new_price = fields.DecimalField(max_digits=12, decimal_places=2)
    percentage_discount = fields.IntField()
    offer_expire_time = fields.DatetimeField(tzinfo=pytz.timezone('Asia/Kolkata'))
    product_name = fields.CharField(max_length = 255, null = False)
    product_image = fields.BinaryField(max_length=1000000, null = False, default = "default.jpg")
    buisness = fields.ForeignKeyField("models.Buisness", related_name="products")
    
user_pydantic = pydantic_model_creator(User, name=User, exclude=("is_verified"))

