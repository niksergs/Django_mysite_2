from django.views.generic import (View,
                                  ListView,
                                  DetailView,
                                  CreateView,
                                  UpdateView,
                                  )
from django.shortcuts import render

# Миксин, который дает возможность добавлять материалы только после авторизации пользователя на сайте.
from django.contrib.auth.mixins import LoginRequiredMixin
# Миксин уведомления для представления обновления материала
from django.contrib.messages.views import SuccessMessageMixin
# Миксин для добавления возможности редактирования статьи только автором или админом
from ..services.mixins import AuthorRequiredMixin

from .models import Post, Category
from .forms import (PostCreateForm,
                    PostUpdateForm,
                    )


# class PostList(View):
#     """PostList на основе класса View"""
#     def get(self, request, *args, **kwargs):
#         posts = Post.objects.all()
#         context = {'posts': posts}
#         return render(request, 'blog/post_list.html', context)
#
#     def post(self, request, *args, **kwargs):
#         pass


class PostListView(ListView):
    """PostList на основе класса ListView"""
    # Название используемой модели
    model = Post
    # По умолчанию ListView ищет шаблон с префиксом имени модели и суффиксом _list.html, если не установлено иное.
    # Это можно переопределить, установив атрибут template_name
    template_name = 'blog/post_list.html'
    # Переопределим имя Queryset по умолчанию object_list, установив атрибут context_object_name = 'posts'.
    # Это помогает иметь более удобное для работы имя.
    context_object_name = 'posts'
    # Ограничение для отображения заданного количества записей на странице
    paginate_by = 5
    # Переопределение вызова модели для использования кастомного менеджера
    queryset = Post.custom.all()

    def get_context_data(self, **kwargs):
        """Функция get_context_data может использоваться для передачи содержимого или параметров вне модели в шаблон,
        в нашем случае мы передаем значение заголовка страницы."""
        context = super().get_context_data(**kwargs)
        context['title'] = 'Главная страница'
        return context


# class PostDetail(View):
#     """PostDetail на основе класса View"""
#     def get(self, request, *args, **kwargs):
#         post = get_object_or_404(Post, pk=kwargs['pk'])
#         context = {'post': post}
#         return render(request, 'blog/post_detail.html', context)


class PostDetailView(DetailView):
    """PostDetail на основе класса DetailView"""
    # Название используемой модели
    model = Post
    # По умолчанию DetailView ищет шаблон с префиксом имени модели и суффиксом _detail.html, если не установлено иное.
    template_name = 'blog/post_detail.html'
    # Переопределим имя Queryset по умолчанию.
    context_object_name = 'post'

    def get_context_data(self, **kwargs):
        # context['title] - наш заголовок передаваемый в шаблон,
        # а self.object.title - это наш объект, т.е наша статья,
        # у которой мы получаем заголовок.
        context = super().get_context_data(**kwargs)
        context['title'] = self.object.title
        return context


class PostFromCategory(ListView):
    """Представление для отображения записей по категориям, на основе класса ListView"""
    template_name = 'blog/post_list.html'
    # Переопределим имя Queryset по умолчанию.
    context_object_name = 'posts'
    # Ограничение для отображения заданного количества записей на странице
    paginate_by = 5
    # Переменная, по которой мы будем работать
    category = None

    def get_queryset(self):
        """Метод обработки запросов, здесь мы получаем категорию по определенному slug,
        а после мы фильтруем запросы статей по категории и возвращаем QuerySet.
        Это работает только для дочерних категорий, если данный объект пустой(при переходе в родительскую категорию),
        то мы получаем все дочерние категории, и выводим все записи из них."""
        self.category = Category.objects.get(slug=self.kwargs['slug'])
        queryset = Post.custom.filter(category__slug=self.category.slug)
        if not queryset:
            sub_cat = Category.objects.filter(parent=self.category)
            queryset = Post.custom.filter(category__in=sub_cat)
        return queryset

    def get_context_data(self, **kwargs):
        """В этом методе передаем <title></title> категории в наш шаблон"""
        context = super().get_context_data(**kwargs)
        context['title'] = f'Записи из категории: {self.category.title}'
        return context


class PostCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    """Представление: создание материалов на сайте"""
    # Указывает модель, с которой будет работать представление PostCreateView.
    model = Post
    # Указываем шаблон, который будет использоваться для отображения формы создания поста.
    template_name = 'blog/post_create.html'
    # Указывает, какую форму использовать для создания новой записи.
    form_class = PostCreateForm
    # Если пользователь не авторизован, то его перенаправляет на указанную страницу
    login_url = 'home'
    # Уведомление при успешном обновлении материала
    success_message = 'Запись была успешно добавлена!'

    def get_context_data(self, **kwargs):
        """Передаем заголовок для <title> нашего шаблона."""
        context = super().get_context_data(**kwargs)
        context['title'] = 'Добавление статьи на сайт'
        return context

    def form_valid(self, form):
        """Проверяем нашу форму, а также сохраняем автором текущего пользователя на странице,
        которого получаем из запроса self.request.user"""
        form.instance.author = self.request.user
        form.save()
        return super().form_valid(form)


class PostUpdateView(AuthorRequiredMixin, SuccessMessageMixin, UpdateView):
    """Представление: обновление материала на сайте"""
    model = Post
    template_name = 'blog/post_update.html'
    context_object_name = 'post'
    form_class = PostUpdateForm
    # Если пользователь не авторизован, то его перенаправляет на указанную страницу
    login_url = 'home'
    # Уведомление при успешном обновлении материала
    success_message = 'Запись была успешно обновлена!'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = f'Обновление статьи: {self.object.title}'
        return context

    def form_valid(self, form):
        # form.instance.updater = self.request.user
        form.save()
        return super().form_valid(form)
