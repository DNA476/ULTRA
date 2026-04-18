from django.contrib import messages
from django.db.models import Q
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, DetailView, ListView, UpdateView

from core.mixins import RoleRequiredMixin
from core.permissions import PROJECT_CRUD_ROLES, PROJECT_VIEW_ROLES, user_has_any_role

from .forms import ClientForm
from .models import Client


class ClientListView(RoleRequiredMixin, ListView):
    model = Client
    template_name = 'clients/client_list.html'
    context_object_name = 'clients'
    paginate_by = 12
    allowed_roles = PROJECT_VIEW_ROLES

    def get_queryset(self):
        queryset = Client.objects.all()
        query = self.request.GET.get('q', '').strip()
        if query:
            queryset = queryset.filter(
                Q(name__icontains=query)
                | Q(contact_person__icontains=query)
                | Q(phone__icontains=query)
                | Q(email__icontains=query)
                | Q(city__icontains=query)
            )
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['current_filters'] = self.request.GET.copy()
        context['can_manage_clients'] = user_has_any_role(self.request.user, PROJECT_CRUD_ROLES)
        return context


class ClientDetailView(RoleRequiredMixin, DetailView):
    model = Client
    template_name = 'clients/client_detail.html'
    context_object_name = 'client'
    allowed_roles = PROJECT_VIEW_ROLES

    def get_queryset(self):
        return Client.objects.prefetch_related('projects')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['can_manage_clients'] = user_has_any_role(self.request.user, PROJECT_CRUD_ROLES)
        return context


class ClientCreateView(RoleRequiredMixin, CreateView):
    model = Client
    form_class = ClientForm
    template_name = 'clients/client_form.html'
    allowed_roles = PROJECT_CRUD_ROLES

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, 'Заказчик создан.')
        return response

    def get_success_url(self):
        return reverse_lazy('clients:client_detail', kwargs={'pk': self.object.pk})


class ClientUpdateView(RoleRequiredMixin, UpdateView):
    model = Client
    form_class = ClientForm
    template_name = 'clients/client_form.html'
    context_object_name = 'client'
    allowed_roles = PROJECT_CRUD_ROLES

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, 'Заказчик обновлен.')
        return response

    def get_success_url(self):
        return reverse_lazy('clients:client_detail', kwargs={'pk': self.object.pk})


class ClientDeleteView(RoleRequiredMixin, DeleteView):
    model = Client
    template_name = 'clients/client_confirm_delete.html'
    context_object_name = 'client'
    success_url = reverse_lazy('clients:client_list')
    allowed_roles = PROJECT_CRUD_ROLES

    def form_valid(self, form):
        messages.success(self.request, 'Заказчик удален.')
        return super().form_valid(form)
