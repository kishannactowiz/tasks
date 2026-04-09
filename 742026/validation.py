from pydantic import BaseModel
from typing import List

class Variant(BaseModel):
    variantName: str
    variantID: int
    variantUrl: str
    variantPrice: float

class VariantOption(BaseModel):
    optionName: str
    optionValues: List[str]

class Product(BaseModel):
    productName: str
    productUrl: str
    productPrice: float
    vender: str
    variantCount: int
    variantopetions: List[VariantOption]
    variants: List[Variant]