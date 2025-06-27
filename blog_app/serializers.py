from rest_framework import serializers
from .models import BlogPost,Comment

class BlogPostSerializer(serializers.ModelSerializer):
    author = serializers.CharField(source='author.username', read_only=True)
    likes = serializers.SerializerMethodField()

    class Meta:
        model = BlogPost
        fields = ['id', 'title', 'content', 'timestamp', 'status', 'author', 'likes']

    def get_likes(self, obj):
        return [user.username for user in obj.likes.all()]



class CommentSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Comment
        fields = '__all__'

    def perform_create(self, serializer):
        if not serializer.is_valid():
            print( "Comment Error:", serializer.errors )
        serializer.save( user=self.request.user, blog_id=self.kwargs['blog_id'] )
