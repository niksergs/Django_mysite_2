from django.views.generic import View, ListView, DetailView
from django.shortcuts import render
from .models import Post


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
    model = Post        # Название нашей модели
    # По умолчанию ListView ищет шаблон с префиксом имени модели и суффиксом _list.html, если не установлено иное.
    # Это можно переопределить, установив атрибут template_name
    template_name = 'blog/post_list.html'
    # Переопределим имя Queryset по умолчанию object_list, установив атрибут context_object_name = 'posts'.
    # Это помогает иметь более удобное для работы имя.
    context_object_name = 'posts'

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
    model = Post        # Название нашей модели
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
