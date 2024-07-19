from ninja import NinjaAPI, Query
from ninja.errors import HttpError
from ninja_simple_jwt.auth.views.api import mobile_auth_router
from ninja_simple_jwt.auth.ninja_auth import HttpJwtAuth
from .models import User, Customer, Address, Metafield, PriceRule, DiscountCode
from .schemas import CustomerOut, CustomerResp, AddressIn, AddressResp, AddressOut, CustomerIn, MetafieldSchema, PriceRuleIn, PriceRuleOut, PriceRuleResp, DiscountCodeIn, DiscountCodeOut, DiscountCodeResp
from typing import List
from django.urls import path
from .views import CustomerAPIView

api = NinjaAPI()
api.add_router("/auth/", mobile_auth_router)
apiAuth = HttpJwtAuth()

@api.get("hello")
def helloWorld(request):
    return {'hello': 'world'}

@api.get("customers.json", auth=apiAuth, response=CustomerResp)
def getAllCustomers(request, ids:str):
    int_ids = ids.split(',')
    customers = Customer.objects.filter(id__in=int_ids)
    return {'customers': customers}

# Single Customer
@api.get('customers/{id_cust}.json', auth=apiAuth, response=CustomerOut)
def getCustomerById(request, id_cust: int):
    customer = Customer.objects.get(pk=id_cust)
    return customer

# Searches for customers that match a supplied query
@api.get('customers/search.json', auth=apiAuth, response=CustomerResp)
def searchCustomers(request, query: str = Query(...)):
    # Extract email, etc from query string
    email_query = query.split(':')[1] if 'email:' in query else None
    first_name_query = query.split(':')[1] if 'first_name:' in query else None
    last_name_query = query.split(':')[1] if 'last_name:' in query else None

    if email_query:
        customers = Customer.objects.filter(user__email=email_query)
    elif first_name_query:
        customers = Customer.objects.filter(user__first_name=first_name_query)
    elif last_name_query:
        customers = Customer.objects.filter(user__last_name=last_name_query)

    return {'customers': customers}

# Count all Customers
@api.get('customers/count.json', auth=apiAuth)
def countCustomers(request):
    customer_count = Customer.objects.count()
    return {"customer_count": customer_count}

# Update Customer
@api.put('customers/{id_cust}.json', auth=apiAuth, response=CustomerOut)
def updateCustomer(request, id_cust: int, data: CustomerIn):
    customer = Customer.objects.get(pk=id_cust)
    user = customer.user
    
    if data.email:
        user.email = data.email
    if data.first_name:
        user.first_name = data.first_name
    if data.last_name:
        user.last_name = data.last_name
    user.save()
    
    if data.phone:
        customer.phone = data.phone
    if data.state:
        customer.state = data.state
    if data.currency:
        customer.currency = data.currency
    customer.save()
    
    return customer

# Delete Customers
@api.delete('customers/{id_cust}.json')
def deleteCust(request, id_cust:int):
    Customer.objects.get(pk=id_cust).delete()
    return {}

# Add Address
@api.post('customers/{id_cust}/addresses.json', auth=apiAuth, response=AddressResp)
def addCustomer(request, id_cust:int, data:AddressIn):
    cust = Customer.objects.get(pk=id_cust)
    newAddr = Address.objects.create(
                customer=cust,
                address1=data.address1,
                address2=data.address2,
                city=data.city,
                province=data.province,
                company=data.company,
                phone=data.phone,
                zip=data.zip
            )
    return {"customer_address": newAddr}

# Retrieves a list of addresses for a customer
@api.get('customers/{id_cust}/addresses.json', auth=apiAuth, response=List[AddressOut])
def getCustomerAddresses(request, id_cust: int):
    addresses = Address.objects.filter(customer_id=id_cust)
    return addresses

# Retrieves details for a single customer address
@api.get('customers/{id_cust}/addresses/{id_addr}.json', auth=apiAuth, response=AddressResp)
def getCustomerAddress(request, id_cust: int, id_addr: int):
    try:
        address = Address.objects.get(customer_id=id_cust, id=id_addr)
        return {"customer_address": address}
    except Address.DoesNotExist:
        raise HttpError(404, "Address not found")

# Set Default Address
@api.put('customers/{id_cust}/addresses/{id_addr}/default.json', auth=apiAuth, response=AddressResp)
def setDefaultAddr(request, id_cust:int, id_addr:int):
    addr = Address.objects.get(pk=id_addr)
    addr.default =True
    addr.save()
    other = Address.objects.filter(customer_id=id_cust).exclude(id=id_addr)
    for data in other:
        data.default = False
        data.save()

    return {"customer_address": addr}

# Delete Address
@api.delete('customers/{id_cust}/addresses/{id_addr}.json')
def deleteAddr(request, id_cust:int, id_addr:int):
    Address.objects.get(pk=id_addr).delete()
    return {}

# Update Address
@api.put('customers/{id_cust}/addresses/{id_addr}.json', auth=apiAuth, response=AddressOut)
def updateCustomerAddress(request, id_cust: int, id_addr: int, data: AddressIn):
    address = Address.objects.get(pk=id_addr, customer_id=id_cust)
    address.address1 = data.address1
    address.address2 = data.address2
    address.city = data.city
    address.province = data.province
    address.company = data.company
    address.phone = data.phone
    address.zip = data.zip
    address.save()
    return address

# Retrieve Metafields by owner_id
@api.get('blogs/{owner_id}/metafields.json', auth=apiAuth, response=List[MetafieldSchema])
def getMetafieldsByOwnerId(request, owner_id: int, owner_resource: str):
    metafields = Metafield.objects.filter(owner_id=owner_id, owner_resource=owner_resource)
    return metafields

# Count Metafields by owner_id
@api.get('blogs/{owner_id}/metafields/count.json', auth=apiAuth)
def countMetafields(request, owner_id: int):
    metafield_count = Metafield.objects.filter(owner_id=owner_id).count()
    return {"metafield_count": metafield_count}

# Retrieve a specific Metafield by owner_id and metafield_id
@api.get('blogs/{owner_id}/metafields/{metafield_id}.json', auth=apiAuth, response=MetafieldSchema)
def getMetafieldById(request, owner_id: int, metafield_id: int):
    try:
        metafield = Metafield.objects.get(owner_id=owner_id, id=metafield_id)
        return metafield
    except Metafield.DoesNotExist:
        raise HttpError(404, "Metafield not found")

# Retrieve Metafields with query parameters
@api.get('blogs/{owner_id}/metafields/search.json', auth=apiAuth, response=List[MetafieldSchema])
def searchMetafields(request, owner_id: int, query: str = Query(...)):
    
    key_query = query.split(':')[1] if 'key:' in query else None
    namespace_query = query.split(':')[1] if 'namespace:' in query else None
    description_query = query.split(':')[1] if 'description:' in query else None

    if key_query:
        metafields = Metafield.objects.filter(owner_id=owner_id, key=key_query)
    elif namespace_query:
        metafields = Metafield.objects.filter(owner_id=owner_id, namespace=namespace_query)
    elif description_query:
        metafields = Metafield.objects.filter(owner_id=owner_id, description=description_query)
    else:
        metafields = Metafield.objects.filter(owner_id=owner_id)

    return {"metafields": metafields}

#Price Rules  
@api.post("/pricerules.json", auth=apiAuth, response=PriceRuleResp)  
def create_price_rule(request, payload: PriceRuleIn):  
    price_rule = PriceRule.objects.create(**payload.dict())  
    return {"price_rule": price_rule}  
  
@api.get("/pricerules.json", auth=apiAuth, response=List[PriceRuleOut])  
def get_price_rules(request):  
    price_rules = PriceRule.objects.all()  
    return {"price_rules": price_rules}  
  
@api.get("/pricerules/{id}.json", auth=apiAuth, response=PriceRuleOut)  
def get_price_rule(request, id: int):  
    price_rule = PriceRule.objects.get(pk=id)  
    return price_rule  
  
@api.get("/pricerules/count.json", auth=apiAuth)  
def get_price_rule_count(request):  
    count = PriceRule.objects.count()  
    return {"count": count}  
  
@api.put("/pricerules/{id}.json", auth=apiAuth, response=PriceRuleResp)  
def update_price_rule(request, id: int, payload: PriceRuleIn):  
    price_rule = PriceRule.objects.get(pk=id)  
    for field, value in payload.dict().items():  
        setattr(price_rule, field, value)  
    price_rule.save()  
    return {"price_rule": price_rule}  
  
@api.delete("/pricerules/{id}.json", auth=apiAuth)  
def delete_price_rule(request, id: int):  
    PriceRule.objects.get(pk=id).delete()  
    return {}  

#Discount Codes
@api.post("/price_rules/{id}/batch.json", auth=apiAuth, response=DiscountCodeResp)  
def create_discount_code(request, payload: DiscountCodeIn):  
   discount_code = DiscountCode.objects.create(**payload.dict())  
   return {"discount_code": discount_code}  

@api.post("/price_rules/{id}/discount_codes.json", auth=apiAuth, response=DiscountCodeOut)  
def create_discount_code_job(request, payload: DiscountCodeIn):  
   discount_code_job = DiscountCode.objects.create(**payload.dict())  
   return {"discount_code_job": discount_code_job} 

@api.get("/discount_codes/count.json", auth=apiAuth)  
def get_discount_code_count(request):  
   count = DiscountCode.objects.count()  
   return {"count": count}  
  
@api.get("/discount_codes/{id}/lookup.json", auth=apiAuth)  
def get_discount_code_location(request, id: int):  
   discount_code = DiscountCode.objects.get(pk=id)  
   return {"location": discount_code.location}
  
@api.put("/price_rules/{id}/discount_codes/{price_rule_id}.json", auth=apiAuth, response=DiscountCodeResp)  
def update_discount_code(request, id: int, payload: DiscountCodeIn):  
   discount_code = DiscountCode.objects.get(pk=id)  
   for field, value in payload.dict().items():  
      setattr(discount_code, field, value)  
   discount_code.save()  
   return {"discount_code": discount_code}  
  
@api.delete("/price_rules/{id}/discount_codes/{price_rule_id}.json", auth=apiAuth)  
def delete_discount_code(request, id: int):  
   DiscountCode.objects.get(pk=id).delete()  
   return {}  
  
urlpatterns = [
    path('customers/', CustomerAPIView.as_view(), name='customer-api'),
]


