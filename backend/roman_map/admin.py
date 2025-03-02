from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, Territorie, Historie, CustomDraw, Answer, Question, Quiz, AncientPlaces
from .forms import TerritoriesJSONForm, HistorieXLSXImportForm, AncientPlacesJSONForm, CustomUserXLSXImportForm
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.urls import path
from django.shortcuts import render, redirect
from django.urls import reverse
from django import forms

# Register your models here.
@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
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

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('upload-xlsx-customuser/', self.upload_file),
        ]
        return custom_urls + urls
    def upload_file(self, request):
        try:
            if request.method == 'POST':
                if "customuser_xlsx_file" in request.POST:
                    form = CustomUserXLSXImportForm(request.POST, request.FILES)
                    if form.is_valid():
                        form.save()
                        self.message_user(request, "Sikeres mentés", level=messages.SUCCESS)
                        return redirect(reverse('admin:roman_map_customuser_changelist'))
                    else:
                        for field, errors in form.errors.items():
                            for error in errors:
                                self.message_user(request, f"Hiba a(z) {field} mezőben: {error}", level=messages.ERROR)
                        self.message_user(request, "A fájl validációja sikertelen!", level=messages.ERROR)
                        return redirect(reverse('admin:roman_map_customuser_changelist'))
                else:
                    self.message_user(request, "Valami hiba történt.", level=messages.ERROR)
            form = CustomUserXLSXImportForm()
            data = {'form':form}
            return render(request, 'admin/roman_map/customuser/import_form.html', data)
        except Exception as e:
            self.message_user(request, f"Hiba: {str(e)}", level=messages.ERROR)

@admin.register(AncientPlaces)
class AncientPlacesAdmin(admin.ModelAdmin):
    list_display = ('id', 'ancient_name', 'modern_name')
    list_filter = ('id', 'ancient_name', 'modern_name')

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('upload-geojson-ancient-places/', self.upload_file),
        ]
        return custom_urls + urls
    def upload_file(self, request):
        try:
            if request.method == 'POST':
                if "places_geojson" in request.POST:
                    form = AncientPlacesJSONForm(request.POST, request.FILES)
                    if form.is_valid():                     
                            form.save()
                            self.message_user(request, "Sikeres mentés", level=messages.SUCCESS)
                            return redirect(reverse('admin:roman_map_ancientplaces_changelist'))
                    else:
                        for field, errors in form.errors.items():
                            for error in errors:
                                self.message_user(request, f"Hiba a(z) {field} mezőben: {error}", level=messages.ERROR)
                        self.message_user(request, "A fájl validációja sikertelen!", level=messages.ERROR)
                        return redirect(reverse('admin:roman_map_ancientplaces_changelist'))
                else:
                    self.message_user(request, "Valami hiba történt.", level=messages.ERROR)
            form = AncientPlacesJSONForm()
            data = {'form': form}
            return render(request, 'admin/roman_map/ancientplaces/import_form.html', data)
        except Exception as e:
            self.message_user(request, f"Hiba: {str(e)}", level=messages.ERROR)
                        


@admin.register(Historie)
class HistoriesAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'date', 'historie_type')
    list_filter = ('id','name', 'date',)
    

    def get_urls(self):
        urls =  super().get_urls()
        custom_urls = [
            path('upload-xlsx-file-from-admin/', self.upload_file),
        ]
        return custom_urls + urls
    
    def upload_file(self, request):
        try:
            if request.method == 'POST':
                if "xlsx_file" in request.POST:
                    form = HistorieXLSXImportForm(request.POST, request.FILES)
                    if form.is_valid():
                            form.save()
                            self.message_user(request, "Sikeres mentés", level=messages.SUCCESS)
                            return redirect(reverse('admin:roman_map_historie_changelist'))                       
                    else:
                        for field, errors in form.errors.items():
                            for error in errors:
                                self.message_user(request, f"Hiba a(z) {field} mezőben: {error}", level=messages.ERROR)
                        self.message_user(request, "A fájl validációja sikertelen!", level=messages.ERROR)
                        return redirect(reverse('admin:roman_map_historie_changelist'))
                else:
                    self.message_user(request, "Valami hiba történt.", level=messages.ERROR)
            form = HistorieXLSXImportForm()
            data = {'form':form}
            return render(request, 'admin/roman_map/historie/import_form.html', data)
        except Exception as e:
            self.message_user(request, f"Hiba: {str(e)}", level=messages.ERROR)


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
#admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Quiz)
admin.site.register(Question)
admin.site.register(CustomDraw)
admin.site.register(Answer)
#admin.site.index_template = 'admin/admin_import_section.html'

