from django.contrib import messages
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, DetailView, ListView, UpdateView

from clients.models import Client
from core.mixins import RoleRequiredMixin
from core.permissions import PROJECT_CRUD_ROLES, PROJECT_VIEW_ROLES, user_has_any_role

from .forms import ParticipationForm, ProjectForm
from .models import Participation, Project


class ProjectListView(RoleRequiredMixin, ListView):
    model = Project
    template_name = 'projects/project_list.html'
    context_object_name = 'projects'
    paginate_by = 12
    allowed_roles = PROJECT_VIEW_ROLES

    def get_queryset(self):
        queryset = Project.objects.select_related('client', 'responsible_employee')
        query = self.request.GET.get('q', '').strip()
        status = self.request.GET.get('status', '').strip()
        project_type = self.request.GET.get('project_type', '').strip()
        client = self.request.GET.get('client', '').strip()
        start_from = self.request.GET.get('start_from', '').strip()
        start_to = self.request.GET.get('start_to', '').strip()

        if query:
            queryset = queryset.filter(
                Q(title__icontains=query)
                | Q(description__icontains=query)
                | Q(client__name__icontains=query)
            )
        if status:
            queryset = queryset.filter(status=status)
        if project_type:
            queryset = queryset.filter(project_type=project_type)
        if client.isdigit():
            queryset = queryset.filter(client_id=int(client))
        if start_from:
            queryset = queryset.filter(start_date__gte=start_from)
        if start_to:
            queryset = queryset.filter(start_date__lte=start_to)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['status_choices'] = Project.Status.choices
        context['type_choices'] = Project.ProjectType.choices
        context['clients'] = Client.objects.all()
        context['current_filters'] = self.request.GET.copy()
        context['can_manage_projects'] = user_has_any_role(self.request.user, PROJECT_CRUD_ROLES)
        return context


class ProjectDetailView(RoleRequiredMixin, DetailView):
    model = Project
    template_name = 'projects/project_detail.html'
    context_object_name = 'project'
    allowed_roles = PROJECT_VIEW_ROLES

    def get_queryset(self):
        return Project.objects.select_related(
            'client',
            'responsible_employee',
        ).prefetch_related(
            'participations__model',
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        can_manage = user_has_any_role(self.request.user, PROJECT_CRUD_ROLES)
        context['can_manage_projects'] = can_manage
        context['participation_form'] = ParticipationForm(project=self.object) if can_manage else None
        return context


class ProjectCreateView(RoleRequiredMixin, CreateView):
    model = Project
    form_class = ProjectForm
    template_name = 'projects/project_form.html'
    allowed_roles = PROJECT_CRUD_ROLES

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, 'Проект создан.')
        return response

    def get_success_url(self):
        return reverse_lazy('projects:project_detail', kwargs={'pk': self.object.pk})


class ProjectUpdateView(RoleRequiredMixin, UpdateView):
    model = Project
    form_class = ProjectForm
    template_name = 'projects/project_form.html'
    context_object_name = 'project'
    allowed_roles = PROJECT_CRUD_ROLES

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, 'Проект обновлен.')
        return response

    def get_success_url(self):
        return reverse_lazy('projects:project_detail', kwargs={'pk': self.object.pk})


class ProjectDeleteView(RoleRequiredMixin, DeleteView):
    model = Project
    template_name = 'projects/project_confirm_delete.html'
    context_object_name = 'project'
    success_url = reverse_lazy('projects:project_list')
    allowed_roles = PROJECT_CRUD_ROLES

    def form_valid(self, form):
        messages.success(self.request, 'Проект удален.')
        return super().form_valid(form)


class ParticipationCreateView(RoleRequiredMixin, CreateView):
    model = Participation
    form_class = ParticipationForm
    allowed_roles = PROJECT_CRUD_ROLES

    def dispatch(self, request, *args, **kwargs):
        self.project = get_object_or_404(Project, pk=kwargs['project_pk'])
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        return redirect('projects:project_detail', pk=self.project.pk)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['project'] = self.project
        return kwargs

    def form_valid(self, form):
        form.instance.project = self.project
        response = super().form_valid(form)
        messages.success(self.request, 'Модель назначена на проект.')
        return response

    def form_invalid(self, form):
        messages.error(self.request, 'Не удалось назначить модель. Проверьте форму.')
        return render(
            self.request,
            'projects/project_detail.html',
            {
                'project': self.project,
                'can_manage_projects': True,
                'participation_form': form,
            },
        )

    def get_success_url(self):
        return reverse_lazy('projects:project_detail', kwargs={'pk': self.project.pk})
