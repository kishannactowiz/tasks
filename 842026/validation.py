from pydantic import BaseModel
from typing import List,Dict,Optional

class AddressInfo(BaseModel):
    full_address: Optional[str]
    region : Optional[str]
    pincode :Optional[int]
    city : Optional[str]
    state: Optional[str]

class Cuisine(BaseModel):
    name: Optional[str]
    url: Optional[str]

class DayTiming(BaseModel):
    open : Optional[str]
    close : Optional[str]

class MenuItem(BaseModel):
    item_id: Optional[int]
    item_name: Optional[str]
    item_slugs: List[str]
    item_url: Optional[str]
    item_description: Optional[str]
    item_price: Optional[float]
    is_veg: Optional[bool]


class MenuCategory(BaseModel):
    category_name:Optional[str]
    items : List[MenuItem]


class Restaurant(BaseModel):
    restaurant_id: Optional[int]
    restaurant_name: Optional[str]
    restaurant_url: Optional[str]
    restaurant_contact: List[str]
    fssai_licence_number: Optional[str]

    address_info: AddressInfo
    cuisines: List[Cuisine]

    timings: Dict[str, DayTiming]   

    menu_categories: List[MenuCategory]