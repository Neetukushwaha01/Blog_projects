from django.http import JsonResponse
from django.shortcuts import render
from django.contrib.auth.models import User
# Create your views here.
from rest_framework import generics, permissions, status
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework.exceptions import NotFound
from rest_framework.views import APIView

from .models import BlogPost
from .serializers import BlogPostSerializer
from rest_framework.pagination import PageNumberPagination

class BlogPostPagination(PageNumberPagination):
    page_size = 10


class BlogPostCreateAPIView(generics.ListCreateAPIView):
    queryset = BlogPost.objects.all().order_by('-timestamp')
    serializer_class = BlogPostSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    pagination_class = BlogPostPagination

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if not serializer.is_valid():
            custom_errors = {field: msgs[0] for field, msgs in serializer.errors.items()}
            return Response({
                "error": " Blog creation failed.",
                "details": custom_errors
            }, status=status.HTTP_400_BAD_REQUEST)

        serializer.save(author=request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)




class BlogPostUpdateAPIView(APIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_object(self, pk):
        try:
            return BlogPost.objects.get(pk=pk)
        except BlogPost.DoesNotExist:
            raise NotFound(detail=" Blog Post Not Found.")

    #  GET (for checking single blog)
    def get(self, request, pk):
        blog = self.get_object(pk)
        serializer = BlogPostSerializer(blog)
        return Response(serializer.data, status=status.HTTP_200_OK)

    #  PUT (for updating blog post)
    def put(self, request, pk):

        blog = self.get_object(pk)
        username = request.user.username if request.user.is_authenticated else "Anonymous"

        if blog.author != request.user:
            return Response(
                {"error": f" User '{username}' is not allowed to update this blog."},
                status=status.HTTP_403_FORBIDDEN
            )

        serializer = BlogPostSerializer(blog, data=request.data)
        if not serializer.is_valid():
            return Response({
                "error": " Blog update failed.",
                "details": serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)

        serializer.save()
        return Response({
            "message": f" Blog updated successfully by user '{username}'.",
            "data": serializer.data
        }, status=status.HTTP_200_OK)

    #  DELETE (for deleting blog post)
    def delete(self, request, pk):
        blog = self.get_object(pk)
        username = request.user.username if request.user.is_authenticated else "Anonymous"

        if blog.author != request.user:
            return Response(
                {"error": f" User '{username}' is not allowed to delete this blog."},
                status=status.HTTP_403_FORBIDDEN
            )

        blog.delete()
        return Response({
            "message": f"🗑️ Blog deleted successfully by user '{username}'."
        }, status=status.HTTP_204_NO_CONTENT)


from .models import Comment
from .serializers import CommentSerializer

class CommentListCreateView(generics.ListCreateAPIView):
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        return Comment.objects.filter(blog_id=self.kwargs['blog_id'])

    def perform_create(self, serializer):
        serializer.save(user=self.request.user, blog_id=self.kwargs['blog_id'])




# blog_app/views.py
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
@api_view(['POST'])
@permission_classes([IsAuthenticated])  #  Login required
def toggle_like(request, pk):
    try:
        blog = BlogPost.objects.get(pk=pk)
        user = request.user

        if user in blog.likes.all():
            blog.likes.remove(user)
            return Response({'message': ' Like removed'})
        else:
            blog.likes.add(user)
            return Response({'message': '❤ Liked'})
    except BlogPost.DoesNotExist:
        return Response({'error': 'Blog not found'}, status=status.HTTP_404_NOT_FOUND)

from django.db.models import Q

class BlogSearchView(generics.ListAPIView):
    serializer_class = BlogPostSerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        query = self.request.query_params.get('q')
        if query:
            return BlogPost.objects.filter(Q(title__icontains=query) | Q(content__icontains=query))
        return BlogPost.objects.none()

class RegisterView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')

        if not username or not password:
            return Response({'error': 'Username and password required'}, status=400)

        if User.objects.filter(username=username).exists():
            return Response({'error': 'Username already exists'}, status=400)

        user = User.objects.create_user(username=username, password=password)
        return Response({'message': 'User registered successfully'}, status=201)

# frontend part____________________________
def home(request):
    return render(request, 'blog_app/index.html')

def blog_crud_page(request):
    return render(request, 'blog_app/blog_crud.html')
def login_page(request):
    return render(request, 'blog_app/login.html')

def register_page(request):
    return render(request, 'blog_app/register.html')



