from django.contrib import admin

from .models import Participation, Project


class ParticipationInline(admin.TabularInline):
    model = Participation
    extra = 1
    autocomplete_fields = ('model',)


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = (
        'title',
        'client',
        'project_type',
        'status',
        'start_date',
        'end_date',
        'budget',
        'responsible_employee',
    )
    list_filter = ('project_type', 'status', 'start_date', 'client')
    search_fields = ('title', 'client__name', 'description', 'notes')
    readonly_fields = ('created_at', 'updated_at')
    autocomplete_fields = ('client', 'responsible_employee')
    inlines = [ParticipationInline]


@admin.register(Participation)
class ParticipationAdmin(admin.ModelAdmin):
    list_display = ('project', 'model', 'status', 'assigned_at')
    list_filter = ('status', 'assigned_at', 'project')
    search_fields = (
        'project__title',
        'model__first_name',
        'model__last_name',
        'comment',
    )
    autocomplete_fields = ('project', 'model')
