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
from .models import Performing
from .models import PerformingDetails
from .models import Family
from .models import Parameter

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
    search_fields = ['station','family']
    list_filter = ['name','family__name']
    list_display = ('station','name','family','description')
    empty_value_display = 'unknown'
    fieldsets = [
        (None,               {'fields': ['station','name','family','description']}),
    ]

    #form = StationModelForm
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
        (None,               {'fields': ['name','model','rev','customer_model','customer_rev','bom']}),
    ]

admin.site.register(Product,ProductAdmin)

#WorkOrder
class WorkOrderDetailsInline(admin.TabularInline):
    model = WorkOrderDetails
    extra = 1

class WorkOrderAdmin(admin.ModelAdmin):
    search_fields = ['name']
    list_filter = ['product','product__name','build_type']
    list_display = ('name','description','product','qty','build_type')
    fieldsets = [
        (None,               {'fields': ['name','description','product','qty','build_type']}),
    ]
    inlines = [WorkOrderDetailsInline]

admin.site.register(WorkOrder,WorkOrderAdmin)

class PerformingDetailsInline(admin.TabularInline):
    model = PerformingDetails
    extra = 1
    exclude = ['value','created_date','user']

class PerformingAdmin(admin.ModelAdmin):
    search_fields = ['sn_wo__sn']
    list_filter = ['station','result','sn_wo__workorder','sn_wo__workorder__product__name']
    list_display = ('get_sn','get_workorder','station','started_date','finished_date','result')
    fieldsets = [
        (None,               {'fields': ['sn_wo','station','result']}),
    ]
    inlines = [PerformingDetailsInline]

    def get_sn(self, obj):
        return obj.sn_wo.sn
    get_sn.short_description = 'Serial number'
    get_sn.admin_order_field = 'sn_wo__sn'

    def get_workorder(self, obj):
        return obj.sn_wo.workorder
    get_workorder.short_description = 'WorkOrder'
    get_workorder.admin_order_field = 'sn_wo__workorder'


    #inlines = [BomDetailsInline]
admin.site.register(Performing,PerformingAdmin)

class FamilyAdmin(admin.ModelAdmin):
    search_fields = ['name']
    list_filter = ['name']
    list_display = ('name','description','created_date','modified_date')
    fieldsets = [
        (None,               {'fields': ['name','description']}),
    ]
    
admin.site.register(Family,FamilyAdmin)


class ParameterAdmin(admin.ModelAdmin):
    search_fields = ['name','group','description']
    list_filter = ['group']
    list_display = ('name','group','description','created_date','modified_date')
    fieldsets = [
        (None,               {'fields': ['name','group','description']}),
    ]
    
admin.site.register(Parameter,ParameterAdmin)