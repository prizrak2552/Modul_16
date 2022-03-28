from django.urls import path

from .views import *

app_name = 'board'

urlpatterns = [
     # posts
     path('', PostList.as_view(), name='post_list'),
     path('<int:pk>', PostDetail.as_view(), name='post_detail'),
     path('create/', PostCreate.as_view(), name='post_create'),
     path('update/<int:post_pk>', PostUpdate.as_view(), name='post_update'),
     path('<int:post_pk>/delete/', PostDelete.as_view(), name='post_delete'),
     # comments
     path('<int:post_pk>/comments', CommentsList.as_view(), name='comments_list'),
     path('<int:post_pk>/create_comment', CommentCreate.as_view(), name='comment_create'),
     path('<int:post_pk>/comments/<int:comment_pk>/accept', CommentAccept.as_view(), name='comment_accept'),
     path('<int:post_pk>/comments/<int:comment_pk>/reject', CommentReject.as_view(), name='comment_reject'),
     path('comments/<int:comment_pk>/delete', CommentDelete.as_view(), name='comment_delete'),
     path('dashboard/', DashboardView.as_view(), name='dashboard'),
     # views
     path('category/<slug:name>', CategoryView.as_view(), name='category'),
     path('by_author/<slug:name>', ByAuthorView.as_view(), name='by_author'),
]