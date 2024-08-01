from django.views.generic import DetailView, UpdateView
from django.db import transaction
from django.urls import reverse_lazy

from .models import Profile
from .forms import UserUpdateForm, ProfileUpdateForm


class ProfileDetailView(DetailView):
    """Представление для просмотра профиля"""
    model = Profile
    # Задаем свойство context_object_name, как profile для использования переменных в шаблоне.
    context_object_name = 'profile'
    template_name = 'accounts/profile_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Добавляем контекст для заголовка страницы
        context['title'] = f"Профиль пользователя: {self.object.user.username}"
        return context


class ProfileUpdateView(UpdateView):
    """Представление для редактирования профиля"""
    model = Profile
    form_class = ProfileUpdateForm
    template_name = 'accounts/profile_edit.html'

    def get_object(self, queryset=None):
        """Передаем текущего пользователя, чтобы не редактировать чужие профили"""
        return self.request.user.profile

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = f"Редактирование профиля пользователя: {self.request.user.username}"
        if self.request.POST:
            context['user_form'] = UserUpdateForm(self.request.POST, instance=self.request.user)
        else:
            context['user_form'] = UserUpdateForm(instance=self.request.user)
        return context

    def form_valid(self,form):
        context = self.get_context_data()
        user_form = context['user_form']
        # Используем transaction.atomic, для корректного сохранения данных двух форм в нашей БД
        with transaction.atomic():
            # Проверяем обе формы на правильность, и сохраняем их
            if all([form.is_valid(), user_form.is_valid()]):
                user_form.save()
                form.save()
            else:
                context.update({'user_form': user_form})
                return self.render_to_response(context)
        return super(ProfileUpdateView, self).form_valid(form)

    def get_success_url(self):
        """После сохранения переходим на страницу нашего профиля"""
        return reverse_lazy('profile_detail', kwargs={'slug': self.object.slug})