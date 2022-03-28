from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views import View
from django.views.generic import ListView, CreateView, UpdateView, DetailView, DeleteView, TemplateView

from .forms import PostCreateForm, CommentCreateForm
from .models import *
from .utils.permissions import IsAuthorMixin, NotIsAuthorMixin


class IndexView(LoginRequiredMixin, TemplateView):
    template_name = 'board/front.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # context['is_not_authors'] = not self.request.user.groups.filter(name = 'authors').exists()

        return context


class PostList(ListView):
    model = Post
    context_object_name = 'post_list'
    queryset = Post.objects.order_by('-datetime')


class PostDetail(DetailView):
    model = Post
    context_object_name = 'post'


class PostCreate(LoginRequiredMixin, CreateView):
    model = Post
    form_class = PostCreateForm
    template_name = 'board/crid/post_create.html'

    def get_success_url(self):
        return reverse('board:post_list')

    def form_valid(self, form):
        post = form.save(commit=False)
        user = self.request.user
        post.author = user
        return super().form_valid(form)


class PostUpdate(IsAuthorMixin, UpdateView):
    model = Post
    pk_url_kwarg = 'post_pk'
    form_class = PostCreateForm
    template_name = 'board/crid/post_create.html'

    def get_success_url(self):
        return reverse('board:post_list')

    def form_valid(self, form):
        messages.success(self.request, 'Success!')
        return super().form_valid(form)


class PostDelete(LoginRequiredMixin, DeleteView):
    model = Post
    template_name = 'board/crid/post_delete.html'
    success_url = '/board/'
    permission_required = ('board.post_delete')
    context_object_name = 'post'

    def get_object(self, **kwargs ):
        post_id = self.kwargs.get('post_pk')
        post = Post.objects.get(pk=post_id)
        return post

class CommentsList(IsAuthorMixin, View):
    def get(self, request, *args, **kwargs):
        post_pk = kwargs['post_pk']
        post = Post.objects.get(pk=post_pk)
        qs = Comment.objects.order_by('datetime').filter(post=post)

        context = {
            'comments': qs,
            'post': post
        }

        return render(request, 'board/comments_list.html', context)


class CommentCreate(NotIsAuthorMixin, View):
    def get(self, request, **kwargs):
        form = CommentCreateForm(request.POST or None)
        post = Post.objects.get(pk=kwargs['post_pk'])

        context = {
            'form': form,
            'post': post
        }

        return render(request, 'board/crid/comment_create.html', context)

    def post(self, request, *args, **kwargs):
        form = CommentCreateForm(request.POST)
        user = request.user
        post_pk = kwargs['post_pk']

        if form.is_valid():
            comment = form.save(commit=False)
            comment.author = user
            comment.post = Post.objects.get(pk=post_pk)
            comment.save()

        return redirect('board:post_list')


class CommentAccept(IsAuthorMixin, View):
    def get(self, request, *args, **kwargs):
        comment_pk = kwargs['comment_pk']

        comment = Comment.objects.get(pk=comment_pk)
        comment.approved = True
        comment.save()

        return redirect(request.META['HTTP_REFERER'])


class CommentReject(IsAuthorMixin, View):
    def get(self, request, *args, **kwargs):
        comment_pk = kwargs['comment_pk']

        comment = Comment.objects.get(pk=comment_pk)
        comment.approved = False
        comment.save()

        return redirect(request.META['HTTP_REFERER'])


class CommentDelete(LoginRequiredMixin, DeleteView):
    model = Comment
    template_name = 'board/crid/comment_delete.html'
    success_url = '/board/'
    permission_required = ('board.comment_delete')
    context_object_name = 'comment'

    def get_object(self, **kwargs ):
        comment_id = self.kwargs.get('comment_pk')
        comment = Comment.objects.get(pk=comment_id)
        return comment


class DashboardView(View):
    def get(self, request, *args, **kwargs):
        context = {
            'posts': request.user.post_set.all(),
        }
        return render(request, 'board/dashboard.html', context)


class CategoryView(ListView):
    def get(self, request, *args, **kwargs):
      category = Category.objects.get(name=kwargs['name'])
      qs = Post.objects.order_by('datetime').filter(category=category)

      context = {
          'category': category,
          'posts': qs,

      }
      return render(request, 'board/category_list.html', context)


class ByAuthorView(ListView):
    def get(self, request, *args, **kwargs):
      author = User.objects.get(username=kwargs['name'])
      qs = Post.objects.order_by('datetime').filter(author = author)

      context = {
          'author': author,
          'posts': qs,
      }
      return render(request, 'board/by_author.html', context)