import os
import sys
sys.path.append(os.path.abspath(os.path.join(__file__, *[os.pardir] * 3)))
os.environ['DJANGO_SETTINGS_MODULE'] = 'shopify.settings'
import django
django.setup()

import json
from customer.models import User, Customer, Address
from metafield.models import Metafield
from discount.models import PriceRule, DiscountCode

filepath = './dummy-data/'

with open(filepath+'customer.json') as jsonfile:
    customers = json.load(jsonfile)
    for cust in customers:
        exitUser = User.objects.filter(email=cust['email']).first()
        if exitUser == None:
            user = User.objects.create_user(username=cust['email'], email=cust['email'],
                                            password=cust['password'],
                                            first_name=cust['first_name'],
                                            last_name=cust['last_name'])
            
            exitCust = Customer.objects.filter(user=user).first()
            if exitCust == None:
                Customer.objects.create(user=user, 
                                        created_at=cust['created_at'],
                                        updated_at=cust['created_at'],
                                        state=cust['state'],
                                        verified_email=cust['verified_email'],
                                        send_email_welcome=cust['send_email_welcome'],
                                        currency=cust['currency'],
                                        phone=cust['phone'])

with open(filepath+'address.json') as jsonfile:
    address = json.load(jsonfile)
    for num, adr in enumerate(address):
        addrExist = Address.objects.filter(id=num+1).first()
        if addrExist == None:
            Address.objects.create(customer_id=adr['customer'],
                                   address1=adr['address1'],
                                   address2=adr['address2'],
                                   city=adr['city'],
                                   province=adr['province'],
                                   country=adr['country'],
                                   company=adr['company'],
                                   phone=adr['phone'],
                                   zip=adr['zip'], default=adr['default'])
            
with open(filepath+'metafield.json') as jsonfile:
    metafields = json.load(jsonfile)
    for meta in metafields:
        Metafield.objects.create(
            created_at=meta['created_at'],
            description=meta['description'],
            key=meta['key'],
            namespace=meta['namespace'],
            owner_id=meta['owner_id'],
            owner_resource=meta['owner_resource'],
            updated_at=meta['updated_at'],
            value=meta['value'],
            type=meta['type']
        )
# Import PriceRule data  
with open(filepath+'pricerule.json') as jsonfile:  
    pricerules = json.load(jsonfile)  
for pricerule in pricerules:  
    PriceRule.objects.create(  
        id=pricerule['id'],  
        title=pricerule['title'],  
        target_type=pricerule['target_type'].strip(),  
        target_selection=pricerule['target_selection'].strip(),  
        allocation_method=pricerule['allocation_method'],  
        value_type=pricerule['value_type'],  
        value_type_list=pricerule['list'],  
        value=pricerule['value'],  
        starts_at=pricerule['starts_at'],  
        ends_at=pricerule['ends_at'],  
        created_at=pricerule['created_at'],  
        updated_at=pricerule['updated_at']  
    )  
 
  
# Import Discount data  
with open(filepath+'discountcode.json') as jsonfile:  
    discountcodes = json.load(jsonfile)  
for discountcode in discountcodes:  
    DiscountCode.objects.create(  
        code=discountcode['code'],  
        created_at=discountcode['created_at'],  
        updated_at=discountcode['updated_at'],  
        id=discountcode['id'],  
        price_rule_id=discountcode['price_rule_id'],  
        usage_count=discountcode['usage_count'],  
        errors=discountcode['errors']  
    )  
