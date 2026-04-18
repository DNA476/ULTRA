from employees.models import EmployeeProfile

ROLE_DIRECTOR = EmployeeProfile.Role.DIRECTOR
ROLE_BOOKER = EmployeeProfile.Role.BOOKER
ROLE_SCOUT = EmployeeProfile.Role.SCOUT
ROLE_ADMIN = EmployeeProfile.Role.ADMIN

FULL_ACCESS_ROLES = (ROLE_DIRECTOR, ROLE_ADMIN)
MODEL_CRUD_ROLES = (ROLE_BOOKER, ROLE_ADMIN)
MODEL_CREATE_ROLES = (ROLE_BOOKER, ROLE_SCOUT, ROLE_ADMIN)
MODEL_VIEW_ROLES = (ROLE_DIRECTOR, ROLE_BOOKER, ROLE_SCOUT, ROLE_ADMIN)
PROJECT_CRUD_ROLES = (ROLE_BOOKER, ROLE_ADMIN)
PROJECT_VIEW_ROLES = (ROLE_DIRECTOR, ROLE_BOOKER, ROLE_ADMIN)
EMPLOYEE_SECTION_ROLES = (ROLE_DIRECTOR, ROLE_ADMIN)
REPORT_FULL_ROLES = (ROLE_DIRECTOR, ROLE_ADMIN)
REPORT_LIMITED_ROLES = (ROLE_DIRECTOR, ROLE_BOOKER, ROLE_ADMIN)
FINANCIAL_REPORT_ROLES = (ROLE_DIRECTOR, ROLE_ADMIN)


def get_user_role(user):
    if not user.is_authenticated or not user.is_active:
        return None
    if user.is_superuser:
        return ROLE_ADMIN
    try:
        profile = user.employee_profile
    except EmployeeProfile.DoesNotExist:
        return None
    if not profile.is_active:
        return None
    return profile.role


def user_has_any_role(user, roles):
    role = get_user_role(user)
    return role in roles


def can_view_financial_reports(user):
    return user_has_any_role(user, FINANCIAL_REPORT_ROLES)


def can_manage_employees(user):
    return user_has_any_role(user, EMPLOYEE_SECTION_ROLES)
