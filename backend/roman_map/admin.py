from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, Territorie, Historie, CustomPolygon, CustomDraw, Point
from .forms import TerritoriesJSONForm, HistorieXLSXImportForm
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.urls import path
from django.shortcuts import render, redirect
from django.urls import reverse

# Register your models here.
@admin.register(Point)
class PointAdmin(admin.ModelAdmin):
    list_display = ('id', 'historie', 'coordinates')

class PointInline(admin.TabularInline):
    model = Point
    extra = 0
    

@admin.register(Historie)
class HistoriesAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'date', 'historie_type')
    list_filter = ('id','name', 'date',)
    inlines = [PointInline]

    def get_urls(self):
        urls =  super().get_urls()
        custom_urls = [
            path('upload-xlsx-file-from-admin/', self.upload_file),
        ]
        return custom_urls + urls
    
    def upload_file(self, request):
        print(request.method)
        if request.method == 'POST':
            print("post")
            if "xlsx_file" in request.POST:
                form = HistorieXLSXImportForm(request.POST, request.FILES)
                if form.is_valid():
                    try:
                        print("errors:")
                        print(form.errors)
                        form.save()
                        print(form.errors)
                        self.message_user(request, "Sikeres mentés", level=messages.SUCCESS)
                        return redirect(reverse('admin:roman_map_historie_changelist'))
                    except Exception as e:
                        self.message_user(request, f"Hiba: {str(e)}", level=messages.ERROR)
                else:
                    self.message_user(request, "A fájl validációja sikertelen!", level=messages.ERROR)
                    return redirect(reverse('admin:roman_map_historie_changelist'))
            else:
                self.message_user(request, "Valami hiba történt.", level=messages.ERROR)
        form = HistorieXLSXImportForm()
        data = {'form':form}
        return render(request, 'admin/roman_map/historie/import_form.html', data)



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
                form = TerritoriesJSONForm(request.POST, request.FILES)
                
                    
                if form.is_valid():
                    try:
                        self.message_user(request, "A feltöltött fájl formátuma megfelelő", level=messages.SUCCESS)
                        form.save()
                        self.message_user(request, "Sikeres mentés", level=messages.SUCCESS)
                        return redirect(reverse('admin:roman_map_territorie_changelist'))
                    except Exception as e:
                        self.message_user(request, f"Hiba: {str(e)}", level=messages.ERROR)
                else:
                    self.message_user(request, "A fájl validációja sikertelen!", level=messages.ERROR)
                    return redirect(reverse('admin:roman_map_territorie_changelist'))
            else:
                self.message_user(request, "Valami hiba történt.", level=messages.ERROR)

        
        form = TerritoriesJSONForm()
        data = {'form':form}
        return render(request, "admin/roman_map/territorie/import_form.html", data)


#admin.site.register(Territorie, TerritorieAdmin)
admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(CustomPolygon)
#admin.site.register(Historie)
admin.site.register(CustomDraw)
#admin.site.register(Point)
#admin.site.index_template = 'admin/admin_import_section.html'

