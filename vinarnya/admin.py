from django.contrib import admin
from vinarnya.models import Language, User, Wine, Color, Country, Type

# Register your models here.
@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('chat_id', 'language')
    list_filter = ('language',)
    search_fields = ('chat_id', 'language')

@admin.register(Language)
class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    list_filter = ('name',)
    search_fields = ('id', 'name')

@admin.register(Wine)
class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'liked', 'image', 'image_id', 'color', 'type', 'country', 'name', 'user')
    list_filter = ('liked', 'color', 'type', 'country', 'name')
    search_fields = ('id', 'liked', 'image', 'image_id', 'color', 'type', 'country', 'name', 'user')

@admin.register(Color)
class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'name_en')
    list_filter = ('name_en',)
    search_fields = ('id', 'name_en')

@admin.register(Type)
class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'name_en')
    list_filter = ('name_en',)
    search_fields = ('id', 'name_en')

@admin.register(Country)
class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'name_en')
    list_filter = ('name_en',)
    search_fields = ('id', 'name_en')