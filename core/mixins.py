from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin

from .permissions import (
    EMPLOYEE_SECTION_ROLES,
    FINANCIAL_REPORT_ROLES,
    FULL_ACCESS_ROLES,
    user_has_any_role,
)


class RoleRequiredMixin(LoginRequiredMixin, UserPassesTestMixin):
    allowed_roles = ()
    raise_exception = True

    def test_func(self):
        return user_has_any_role(self.request.user, self.allowed_roles)


class DirectorOrAdminRequiredMixin(RoleRequiredMixin):
    allowed_roles = FULL_ACCESS_ROLES


class EmployeeSectionRequiredMixin(RoleRequiredMixin):
    allowed_roles = EMPLOYEE_SECTION_ROLES


class FinancialReportRequiredMixin(RoleRequiredMixin):
    allowed_roles = FINANCIAL_REPORT_ROLES
