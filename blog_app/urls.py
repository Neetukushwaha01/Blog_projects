
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from django.urls import path
from .views import*

urlpatterns = [
    # use frontend part page

    path( 'register/', register_page, name='register_page' ),
    path( 'login/', login_page, name='login_page' ),
    path( '', home, name='home' ),
    path( 'blogPost/', blog_crud_page, name='blog-crud-ui' ),
    path('api/search/', BlogSearchView.as_view(), name='blog-search'),
    # use API urls
    path('api/register/', RegisterView.as_view(), name='register'),
    path('api/posts/', BlogPostCreateAPIView.as_view(), name='post-list-create'),
    path('api/posts/<int:pk>/', BlogPostUpdateAPIView.as_view(), name='post-detail'),
    path( 'api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair' ),
    path( 'token/refresh/', TokenRefreshView.as_view(), name='token_refresh' ),


    #  its (Optional) API
    path('api/posts/<int:pk>/like/', toggle_like, name='toggle-like'),
    path('api/posts/<int:blog_id>/comments/', CommentListCreateView.as_view(), name='comments'),

    # path('create-test-posts/', create_dummy_blogs, name='create-test-posts'), # dont use this   only use for post add


]