from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Sum
from django.utils import timezone
from django.views.generic import TemplateView

from employees.models import EmployeeProfile
from models_app.models import ModelCard
from projects.models import Project

from .permissions import can_manage_employees, can_view_financial_reports


class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'core/dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        today = timezone.localdate()

        current_month_revenue = Project.objects.filter(
            status=Project.Status.COMPLETED,
            end_date__year=today.year,
            end_date__month=today.month,
        ).aggregate(total=Sum('budget'))['total'] or 0

        context.update(
            {
                'total_models': ModelCard.objects.count(),
                'active_models': ModelCard.objects.filter(status=ModelCard.Status.ACTIVE).count(),
                'archived_models': ModelCard.objects.filter(status=ModelCard.Status.ARCHIVED).count(),
                'contract_models': ModelCard.objects.filter(status=ModelCard.Status.ON_CONTRACT).count(),
                'open_projects': Project.objects.filter(
                    status__in=[Project.Status.NEW, Project.Status.IN_PROGRESS],
                ).count(),
                'current_month_revenue': current_month_revenue,
                'can_view_revenue': can_view_financial_reports(self.request.user),
                'can_manage_employees': can_manage_employees(self.request.user),
                'employees_count': EmployeeProfile.objects.filter(is_active=True, user__is_active=True).count(),
                'latest_models': ModelCard.objects.select_related('added_by').order_by('-created_at')[:5],
                'latest_projects': Project.objects.select_related('client', 'responsible_employee').order_by('-created_at')[:5],
            }
        )
        return context
