from django.db.models import Count, Q, Sum
from django.utils import timezone
from django.views.generic import TemplateView

from core.mixins import RoleRequiredMixin
from core.permissions import (
    REPORT_LIMITED_ROLES,
    can_view_financial_reports,
    can_view_staff_workload_reports,
)
from employees.models import EmployeeProfile
from models_app.models import ModelCard
from projects.models import Participation, Project

from .forms import ReportPeriodForm


class ReportsView(RoleRequiredMixin, TemplateView):
    template_name = 'reports/reports.html'
    allowed_roles = REPORT_LIMITED_ROLES

    def get_period_form(self):
        return ReportPeriodForm(self.request.GET or None)

    def get_period(self, form):
        today = timezone.localdate()
        date_from = form.cleaned_data.get('date_from') or today.replace(day=1)
        date_to = form.cleaned_data.get('date_to') or today
        return date_from, date_to

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        form = self.get_period_form()

        if form.is_valid():
            date_from, date_to = self.get_period(form)
        else:
            today = timezone.localdate()
            date_from, date_to = today.replace(day=1), today

        can_view_finance = can_view_financial_reports(self.request.user)
        can_view_staff = can_view_staff_workload_reports(self.request.user)

        model_popularity = ModelCard.objects.annotate(
            participations_count=Count(
                'participations',
                filter=Q(
                    participations__project__start_date__gte=date_from,
                    participations__project__start_date__lte=date_to,
                ),
            ),
            approved_count=Count(
                'participations',
                filter=Q(
                    participations__status=Participation.Status.APPROVED,
                    participations__project__start_date__gte=date_from,
                    participations__project__start_date__lte=date_to,
                ),
            ),
        ).order_by('-participations_count', '-approved_count', 'last_name', 'first_name')

        financial_report = None
        if can_view_finance:
            completed_projects = Project.objects.filter(
                status=Project.Status.COMPLETED,
                end_date__gte=date_from,
                end_date__lte=date_to,
            )
            financial_report = completed_projects.aggregate(
                total_revenue=Sum('budget'),
                projects_count=Count('id'),
            )
            financial_report['total_revenue'] = financial_report['total_revenue'] or 0

        staff_workload = None
        if can_view_staff:
            staff_workload = EmployeeProfile.objects.select_related('user').annotate(
                open_projects_count=Count(
                    'projects',
                    filter=Q(
                        projects__status__in=[Project.Status.NEW, Project.Status.IN_PROGRESS],
                        projects__start_date__gte=date_from,
                        projects__start_date__lte=date_to,
                    ),
                ),
                completed_projects_count=Count(
                    'projects',
                    filter=Q(
                        projects__status=Project.Status.COMPLETED,
                        projects__end_date__gte=date_from,
                        projects__end_date__lte=date_to,
                    ),
                ),
            ).order_by('-open_projects_count', '-completed_projects_count', 'user__last_name')

        context.update(
            {
                'form': form,
                'date_from': date_from,
                'date_to': date_to,
                'model_popularity': model_popularity,
                'financial_report': financial_report,
                'staff_workload': staff_workload,
                'can_view_finance': can_view_finance,
                'can_view_staff': can_view_staff,
            }
        )
        return context
