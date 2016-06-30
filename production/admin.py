from django.contrib import admin

# Register your models here.
from .models import Bom
from .models import BomDetails
from .models import Station
from .models import Routing
from .models import RoutingDetails
from .models import Product
from .models import WorkOrder
from .models import WorkOrderDetails
from .forms import StationModelForm

class BomDetailsInline(admin.TabularInline):
    model = BomDetails
    extra = 1

class BomAdmin(admin.ModelAdmin):
    search_fields = ['name']
    list_filter = ['model']
    list_display = ('name','model','rev','description')
    fieldsets = [
        (None,               {'fields': ['name','model','rev','description']}),
    ]
    inlines = [BomDetailsInline]

admin.site.register(Bom,BomAdmin)

class StationAdmin(admin.ModelAdmin):
    search_fields = ['station']
    list_filter = ['name']
    list_display = ('station','name','description')
    empty_value_display = 'unknown'
    form = StationModelForm
    # search_fields = ['station']
    # list_filter = ['name']
    # list_display = ('station','name','description')
    # fieldsets = [
    #     (None,               {'fields': ['station','name','description']}),
    # ]
    # form = StationModelForm

admin.site.register(Station,StationAdmin)


#Routing
class RoutingDetailsInline(admin.TabularInline):
    model = RoutingDetails
    extra = 1

class RoutingAdmin(admin.ModelAdmin):
    search_fields = ['name']
    list_filter = ['name']
    list_display = ('name','description')
    fieldsets = [
        (None,               {'fields': ['name','description']}),
    ]
    inlines = [RoutingDetailsInline]

admin.site.register(Routing,RoutingAdmin)

#Product
class ProductAdmin(admin.ModelAdmin):
    search_fields = ['name']
    list_filter = ['model','customer_model']
    list_display = ('name','model','rev','customer_model','customer_rev')
    fieldsets = [
        (None,               {'fields': ['name','model','rev','customer_model','customer_rev']}),
    ]

admin.site.register(Product,ProductAdmin)

#WorkOrder
class WorkOrderDetailsInline(admin.TabularInline):
    model = WorkOrderDetails
    extra = 1

class WorkOrderAdmin(admin.ModelAdmin):
    search_fields = ['name']
    list_filter = ['product','build_type']
    list_display = ('name','description','product','qty','build_type')
    fieldsets = [
        (None,               {'fields': ['name','description','product','qty','build_type']}),
    ]
    inlines = [WorkOrderDetailsInline]

admin.site.register(WorkOrder,WorkOrderAdmin)