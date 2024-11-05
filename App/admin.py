from django.contrib import admin
from . models import Vendor,Category,Product,Cart
admin.site.register(Vendor)  
admin.site.register(Category)
admin.site.register(Product)
admin.site.register(Cart)