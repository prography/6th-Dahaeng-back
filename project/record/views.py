from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
#from django.views.decorators.vary import vary_on_cookie
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework import status

from .models import Post, Question
from .serializers import PostSerializer, QuestionSerializer
from .filters import DynamicSearchFilter
from config.permissions import MyIsAuthenticated

from django.http import Http404

# random happy-question
import random

# Restrict the post to be updated only on the day.
#from datetime import datetime
#from django.utils import timezone

def pick_number():
    count = Question.objects.all().count()
    if count < 1:
        return 0
    return random.randint(1, count)

# TODO
# permission_classes = [MyIsAuthenticated, ]
class PostList(ListAPIView):
    """
    List all happy-record of a now-user
    """
    permission_classes = [AllowAny, ]
    serializer_class = PostSerializer
    filter_backends = (DynamicSearchFilter, )

    def get_queryset(self):
        return Post.objects.all().filter(profile=self.request.user.pk)

class PostCreateView(APIView):
    permission_classes = [AllowAny, ]
    
    # TODO
    # 자정 기준으로 바꿔주기 (현재 60초)
    @method_decorator(cache_page(60))
    #@method_decorator(vary_on_cookie)
    def get(self, request):
        qid = pick_number()
        question = Question.objects.all().filter(id = qid)
        serializer = QuestionSerializer(question, many=True)
        response = Response(serializer.data, status=status.HTTP_201_CREATED)
        #response.set_cookie('my_question', qid)
        return response
    
    def post(self, request):
        '''
        {
            "question": "question 예제 - 수동으로 입력",
            "detail": "일기 내용"
        }
        '''
        data = request.data
        data['profile'] = request.user.email
        #data['question'] = request.COOKIES.get('my_question')
        serializer = PostSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response({
                "response": "success", 
                "message": "성공적으로 일기를 업로드하였습니다."
                }, status=status.HTTP_201_CREATED)
        return Response({
            "response": "error",
            "message": serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)

class PostDetail(APIView):
    """
    Retrieve a happy-record instance for a specific date
    """
    permission_classes = [AllowAny, ]
    
    def get_object(self, pk):
        try:
            return Post.objects.get(pk=pk)
        except:
            raise Http404

    def get(self, request, pk, format=None):
        post = self.get_object(pk)
        serializer = PostSerializer(post)
        return Response(serializer.data)
    
    # TODO
    # 같은 날짜에만 수정할 수 있도록 구현하기!!
    def put(self, request, pk, format=None):
        post = self.get_object(pk)
        data = request.data
        data['profile'] = request.user.email
        serializer = PostSerializer(post, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({
                "response": "success", 
                "message": serializer.data
                })
        return Response(serializer.error, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        post = self.get_object(pk)
        post.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)