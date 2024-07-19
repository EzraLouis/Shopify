from django.db import models
from django.contrib.auth.models import User
from pydantic import BaseModel

class Customer(models.Model):
    STATE_CHOICES = [('disabled', 'disabled'), ('invited', 'invited'),
                     ('enabled', 'enabled'), ('declined', 'declined')]

    user = models.ForeignKey(User, on_delete=models.RESTRICT, unique=True)
    phone = models.CharField(max_length=100, null=True,blank=True)
    verified_email = models.BooleanField(default=False)
    send_email_welcome = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    state = models.CharField()
    currency = models.CharField(max_length=10)

    @property
    def order_counts(self):
        return 0

class Address(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    address1 = models.TextField()
    address2 = models.TextField(null=True, blank=True)
    city = models.CharField(max_length=250)
    province = models.CharField(max_length=250)
    country = models.CharField(max_length=250)
    phone = models.CharField(max_length=100, null=True, blank=True)
    zip = models.CharField(max_length=20)
    company = models.CharField(max_length=200)
    default = models.BooleanField(default=False)

    @property
    def name(self):
        return self.customer.user.first_name+" "+self.customer.user.last_name

class Metafield(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    description = models.TextField()
    key = models.CharField(max_length=64)
    namespace = models.CharField(max_length=255)
    owner_id = models.BigIntegerField()
    owner_resource = models.CharField(max_length=255)
    updated_at = models.DateTimeField(auto_now=True)
    value = models.TextField()
    type = models.CharField(max_length=255)

    def _str_(self):
        return f'{self.namespace}:{self.key}'

    class Meta:
        unique_together = ('namespace', 'key', 'owner_id', 'owner_resource')

class PriceRule(models.Model):
    title = models.CharField(max_length=255)
    target_type = models.CharField(max_length=255)
    target_selection = models.CharField(max_length=255)
    allocation_method = models.CharField(max_length=255)
    value_type = models.CharField(max_length=255)
    value = models.IntegerField(null=True, blank=True)
    customer_segment_prerequisite = models.CharField(max_length=255, null=True, blank=True)
    prerequisite_quantity_range = models.PositiveIntegerField(null=True, blank=True)
    prerequisite_shipping_price_range = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    prerequisite_subtotal_range = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    prerequisite_to_entitlement_quantity_ratio = models.PositiveIntegerField(null=True, blank=True)
    prerequisite_to_entitlement_purchase = models.PositiveIntegerField(null=True, blank=True)
    starts_at = models.DateTimeField()
    ends_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

  
class DiscountCode(models.Model):  
    code = models.CharField(max_length=20, unique=True)  
    created_at = models.DateTimeField()  
    updated_at = models.DateTimeField()  
    id = models.IntegerField(primary_key=True)  
    price_rule = models.ForeignKey('PriceRule', on_delete=models.CASCADE)  
    usage_count = models.IntegerField()  
    errors = models.TextField()  

