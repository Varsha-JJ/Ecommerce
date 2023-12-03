import csv
from django.contrib import admin 
from django.http import HttpResponse
from .models import Product,Category,Color,Size,Filter_Price,Payment,OrderPlaced,Wishlist,MainCategory
# Register your models here.
# admin.site.register(Product)
# admin.site.register(Category)
# admin.site.register(Filter_Price)
admin.site.register(Size)
admin.site.register(Payment) 
# admin.site.register(MainCategory)
# admin.site.register(OrderPlaced)
# admin.site.register(Sell_product)


def export_productdetail(modeladmin, request, queryset):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="productdetail.csv"'
    writer = csv.writer(response)
    writer.writerow(['Name','Category','Price'])
    product = queryset.values_list('name','category','price')
    for i in product:
        writer.writerow(i)
    return response


export_productdetail.short_description = 'Export to csv'


class productAdmin(admin.ModelAdmin):
    list_display = ('name','price','thumbnail_preview','stock')
    actions = [export_productdetail]
    search_fields = ['name','price']
    def thumbnail_preview(self, obj):
        return obj.thumbnail_preview

    thumbnail_preview.short_description = 'Image Preview'
    thumbnail_preview.allow_tags = True
   
admin.site.register(Product, productAdmin)


class proColor(admin.ModelAdmin):
    list_display = ['name','code']
    actions = [export_productdetail]
    search_feilds = ('name')

admin.site.register(Color, proColor)  

class SubcategoryAdmin(admin.ModelAdmin):
    list_display = ['title','category']

admin.site.register(Category,SubcategoryAdmin)  


class proPrice(admin.ModelAdmin):
    list_display = ['price']
    actions = [export_productdetail]

admin.site.register(Filter_Price,proPrice)
 
class maincat(admin.ModelAdmin):
    list_display = ['item']
    # actions = [export_categorydetail]

admin.site.register(MainCategory,maincat)

def export_orderdetail(modeladmin, request, queryset):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="orderdetail.csv"'
    writer = csv.writer(response)
    writer.writerow(['User','Product name','Quantity'])
    product = queryset.values_list('user','product','quantity')
    for i in product:
        writer.writerow(i)
    return response

class orderplacedAdmin(admin.ModelAdmin):
    list_display = ['user','product','quantity']
    search_feilds = ('user','product')
    actions = [export_orderdetail]
    def render_change_form(self, request, context, add=False, change=False, form_url='', obj=None):
        context.update({
            'show_save': False,
            'show_save_and_continue': False,
            'show_save_and_add_another': False,
            'show_delete': False,
            'Groups': False
        })
        return super().render_change_form(request, context, add, change, form_url, obj)

admin.site.register(OrderPlaced, orderplacedAdmin) 
# class orderplacedAdmin(admin.ModelAdmin):
#     list_display = ('product')
#     actions = [export_orderdetail]
#     search_fields = ['product']

# admin.site.register(OrderPlaced, orderplacedAdmin)
     
    