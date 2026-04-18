from django.views.generic import DetailView, ListView

from core.mixins import EmployeeSectionRequiredMixin

from .models import EmployeeProfile


class EmployeeListView(EmployeeSectionRequiredMixin, ListView):
    model = EmployeeProfile
    template_name = 'employees/employee_list.html'
    context_object_name = 'employees'
    paginate_by = 20

    def get_queryset(self):
        return EmployeeProfile.objects.select_related('user')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['role_choices'] = EmployeeProfile.Role.choices
        return context


class EmployeeDetailView(EmployeeSectionRequiredMixin, DetailView):
    model = EmployeeProfile
    template_name = 'employees/employee_detail.html'
    context_object_name = 'employee'

    def get_queryset(self):
        return EmployeeProfile.objects.select_related('user').prefetch_related('projects')
