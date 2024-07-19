from ninja import Schema, ModelSchema, FilterSchema, Field
from datetime import datetime
from typing import Optional, List, Self
from pydantic import model_validator

from customer.models import Customer, Address, Metafield, DiscountCode, PriceRule

class AddressIn(Schema):
    customer_id: int
    address1: str
    address2: Optional[str] = ''
    city: str
    first_name: Optional[str] = ''
    last_name: Optional[str] = ''
    phone: Optional[str] = ''
    province: str
    country: str
    zip: str
    company: str
    name: Optional[str] = ''

class AddressOut(Schema):
    id: int
    customer_id: int
    first_name: str = Field(alias='customer.user.first_name')
    last_name: str = Field(alias='customer.user.last_name')
    company: str
    address1: str
    address2: str
    city: str
    province: str
    zip: str
    phone: Optional[str] = ''
    name: str
    default: bool

class AddressResp(Schema):
    customer_address: AddressOut

class CustomerIn(Schema):
    email: Optional[str] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    state: Optional[str] = None
    phone: Optional[str] = None
    currency: Optional[str] = None

class CustomerOut(Schema):
    id: int
    email: str = Field(alias='user.email')
    created_at: datetime
    updated_at: datetime
    first_name: str = Field(alias='user.first_name')
    last_name: str = Field(alias='user.last_name')
    order_counts: int
    state: str
    verified_email: bool
    currency: str
    phone: str
    addresses: Optional[List[AddressOut]] = Field(alias='address_set')

class CustomerResp(Schema):
    customers: List[CustomerOut]

class MetafieldSchema(Schema):
    id: int
    created_at: datetime
    description: str
    key: str
    namespace: str
    owner_id: int
    owner_resource: str
    updated_at: datetime
    value: str
    type: str

    class Config:
        orm_mode = True

class MetafieldCreate(Schema):
    id: int
    description: str
    key: str
    namespace: str
    owner_id: int
    owner_resource: str
    created_at: datetime
    updated_at: datetime
    value: str
    type: str  

class DiscountCodeIn(Schema):
    price_rule_id: int
    code: str
    usage_count: Optional[int] = 0
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

class DiscountCodeOut(Schema):
    id: int
    price_rule_id: int
    code: str
    usage_count: int = 0
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    class Config:
        orm_mode = True

class DiscountCodeResp(Schema):
    discount_code: DiscountCodeOut

class PriceRuleIn(Schema):
    title: str
    target_type: str
    target_selection: str
    allocation_method: str
    value_type: str
    value: float
    starts_at: datetime
    ends_at: Optional[datetime] = None

class PriceRuleOut(Schema):
    id: int
    title: str
    target_type: str
    target_selection: str
    allocation_method: str
    value_type: str
    value: int
    customer_segment_prerequisite: Optional[str] = ''
    prerequisite_quantity_range: Optional[int] = None
    prerequisite_shipping_price_range: Optional[float] = None
    prerequisite_subtotal_range: Optional[float] = None
    prerequisite_to_entitlement_quantity_ratio: Optional[int] = None
    prerequisite_to_entitlement_purchase: Optional[int] = None
    starts_at: datetime
    ends_at: Optional[datetime] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    class Config:
        orm_mode = True

class PriceRuleResp(Schema):
    price_rule: PriceRuleOut

class PriceRuleWithDiscountCodesOut(PriceRuleOut):
    discount_codes: List[DiscountCodeOut] = []

class PriceRuleWithDiscountCodesResp(Schema):
    price_rule: PriceRuleWithDiscountCodesOut