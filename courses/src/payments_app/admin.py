from django.contrib import admin
from payments_app.models import Card, Customer, Payment

admin.site.register(Card)
admin.site.register(Customer)
admin.site.register(Payment)
