from django.contrib import admin

from .models import *

admin.site.site_header="IIT Indore"
admin.site.site_title="Welcome to IIT Indore Covid maddad"
admin.site.site_footer="IIT Indore footer"
admin.site.index_title="Covid Supplier varfiaction administration"

admin.site.register(City)
admin.site.register(Resources)

class SupplierAdmin(admin.ModelAdmin):
	list_display=('name','Number','status','date_created','email')
	list_filter=('city','status')
	search_fields=('Number','name')

admin.site.register(Supplier,SupplierAdmin)
# admin.site.register(SupplierAdmin)