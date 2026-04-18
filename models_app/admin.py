from django.contrib import admin

from .models import ModelCard, ModelPhoto


class ModelPhotoInline(admin.TabularInline):
    model = ModelPhoto
    extra = 1


@admin.register(ModelCard)
class ModelCardAdmin(admin.ModelAdmin):
    list_display = (
        'full_name',
        'category',
        'status',
        'city',
        'height',
        'created_at',
        'added_by',
    )
    list_filter = ('category', 'status', 'city', 'created_at')
    search_fields = ('first_name', 'last_name', 'phone', 'email', 'city')
    readonly_fields = ('created_at', 'updated_at')
    inlines = [ModelPhotoInline]

    @admin.display(description='Модель')
    def full_name(self, obj):
        return str(obj)


@admin.register(ModelPhoto)
class ModelPhotoAdmin(admin.ModelAdmin):
    list_display = ('model', 'caption', 'uploaded_at')
    list_filter = ('uploaded_at',)
    search_fields = ('model__first_name', 'model__last_name', 'caption')
