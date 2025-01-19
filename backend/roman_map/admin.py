from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, Territorie, Historie
from .forms import TerritoriesJSONForm
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.urls import path
from django.shortcuts import render

# Register your models here.

class CustomUserAdmin(UserAdmin):
    list_display = (
        'username', 'email', 'first_name', 'last_name', 'is_staff',
        'tanar', 'tanulo')
    
    fieldsets = (
        (None, {
            'fields': ('username', 'password')
        }),
        ('Additional info', {
            'fields': ('tanar', 'tanulo')
        }),
        ('Personal info', {
            'fields': ('first_name', 'last_name', 'email')
        }),
        ('Permissions', {
            'fields': (
                'is_active', 'is_staff', 'is_superuser',
                'groups', 'user_permissions'
                )
        }),
        ('Important dates', {
            'fields': ('last_login', 'date_joined')
        }),
    )

    add_fieldsets = (
        (None, {
            'fields': ('username', 'password1', 'password2')
        }),
        ('Additional info', {
            'fields': ('tanar', 'tanulo')
        }),
        ('Personal info', {
            'fields': ('first_name', 'last_name', 'email')
        }),
        ('Permissions', {
            'fields': (
                'is_active', 'is_staff', 'is_superuser',
                'groups', 'user_permissions'
                )
        }),
        ('Important dates', {
            'fields': ('last_login', 'date_joined')
        }),
    )

@admin.register(Territorie)
class TerritorieAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'start_date', 'end_date', 'color')
    list_filter = ('name', 'start_date', 'end_date')

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('upload-file-from-admin/', self.upload_file),
        ]
        return custom_urls + urls
    
    def upload_file(self, request):
        if request.method == 'POST':
            if "json_file" in request.POST:
                try:
                    form = TerritoriesJSONForm(request.POST, request.FILES)
                    if form.is_valid():
                        form.save()
                        self.message_user(request, "Sikeres importálás", level=messages.SUCCESS)
                except Exception as e:
                    print("hiba:"+str(e))
        
        form = TerritoriesJSONForm()
        data = {'form':form}
        return render(request, "admin/roman_map/territorie/import_form.html", data)


#admin.site.register(Territorie, TerritorieAdmin)
admin.site.register(CustomUser, CustomUserAdmin)
#admin.site.register(Territorie)
admin.site.register(Historie)
#admin.site.index_template = 'admin/admin_import_section.html'

