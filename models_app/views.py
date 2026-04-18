from django.contrib import messages
from django.db.models import Q
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, DetailView, ListView, UpdateView

from core.mixins import RoleRequiredMixin
from core.permissions import (
    MODEL_CREATE_ROLES,
    MODEL_CRUD_ROLES,
    MODEL_VIEW_ROLES,
    user_has_any_role,
)

from .forms import ModelCardForm
from .models import ModelCard


class ModelCardListView(RoleRequiredMixin, ListView):
    model = ModelCard
    template_name = 'models_app/model_list.html'
    context_object_name = 'models'
    paginate_by = 12
    allowed_roles = MODEL_VIEW_ROLES

    def get_queryset(self):
        queryset = ModelCard.objects.select_related('added_by')

        query = self.request.GET.get('q', '').strip()
        category = self.request.GET.get('category', '').strip()
        status = self.request.GET.get('status', '').strip()
        height_min = self.request.GET.get('height_min', '').strip()
        height_max = self.request.GET.get('height_max', '').strip()
        has_experience = self.request.GET.get('has_experience', '').strip()
        sort = self.request.GET.get('sort', 'name').strip()

        if query:
            queryset = queryset.filter(
                Q(first_name__icontains=query)
                | Q(last_name__icontains=query)
                | Q(phone__icontains=query)
                | Q(email__icontains=query)
            )
        if category:
            queryset = queryset.filter(category=category)
        if status:
            queryset = queryset.filter(status=status)
        if height_min.isdigit():
            queryset = queryset.filter(height__gte=int(height_min))
        if height_max.isdigit():
            queryset = queryset.filter(height__lte=int(height_max))
        if has_experience == 'yes':
            queryset = queryset.exclude(experience='')
        elif has_experience == 'no':
            queryset = queryset.filter(experience='')

        ordering = {
            'name': ['last_name', 'first_name'],
            '-name': ['-last_name', '-first_name'],
            'created': ['created_at'],
            '-created': ['-created_at'],
        }.get(sort, ['last_name', 'first_name'])
        return queryset.order_by(*ordering)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category_choices'] = ModelCard.Category.choices
        context['status_choices'] = ModelCard.Status.choices
        context['current_filters'] = self.request.GET.copy()
        context['can_create_model'] = user_has_any_role(self.request.user, MODEL_CREATE_ROLES)
        return context


class ModelCardDetailView(RoleRequiredMixin, DetailView):
    model = ModelCard
    template_name = 'models_app/model_detail.html'
    context_object_name = 'model_card'
    allowed_roles = MODEL_VIEW_ROLES

    def get_queryset(self):
        return ModelCard.objects.select_related('added_by').prefetch_related('photos')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['can_edit_model'] = user_has_any_role(self.request.user, MODEL_CRUD_ROLES)
        return context


class ModelCardCreateView(RoleRequiredMixin, CreateView):
    model = ModelCard
    form_class = ModelCardForm
    template_name = 'models_app/model_form.html'
    allowed_roles = MODEL_CREATE_ROLES

    def form_valid(self, form):
        form.instance.added_by = self.request.user
        response = super().form_valid(form)
        messages.success(self.request, 'Анкета модели создана.')
        return response

    def get_success_url(self):
        return self.object.get_absolute_url() if hasattr(self.object, 'get_absolute_url') else reverse_lazy('models_app:model_detail', kwargs={'pk': self.object.pk})


class ModelCardUpdateView(RoleRequiredMixin, UpdateView):
    model = ModelCard
    form_class = ModelCardForm
    template_name = 'models_app/model_form.html'
    context_object_name = 'model_card'
    allowed_roles = MODEL_CRUD_ROLES

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, 'Анкета модели обновлена.')
        return response

    def get_success_url(self):
        return reverse_lazy('models_app:model_detail', kwargs={'pk': self.object.pk})


class ModelCardDeleteView(RoleRequiredMixin, DeleteView):
    model = ModelCard
    template_name = 'models_app/model_confirm_delete.html'
    context_object_name = 'model_card'
    success_url = reverse_lazy('models_app:model_list')
    allowed_roles = MODEL_CRUD_ROLES

    def form_valid(self, form):
        messages.success(self.request, 'Анкета модели удалена.')
        return super().form_valid(form)
