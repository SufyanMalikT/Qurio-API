from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from .models import CustomUser, Questions, Answers, Vote, Tags
from .serializers import CustomUserSerializer, QuestionsSerializer, AnswerSerializer, VoteSerializer, TagSerializer
from rest_framework.decorators import action
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer, TokenRefreshSerializer
from rest_framework import status, filters 
from .permissions import CustomUserPermissions, QuestionPermission, AnswerPermission, TagsPermission
from rest_framework.pagination import PageNumberPagination
# Create your views here.

class CookieTokenRefreshView(TokenRefreshView):
    serializer_class = TokenRefreshSerializer

    def post(self, request, *args, **kwargs):
        refresh_token = request.COOKIES.get('refresh_token')
        if not refresh_token:
            return Response({'errors':'No Resfresh token provided'},status=status.HTTP_401_UNAUTHORIZED)
        serializer = self.get_serializer(data={'refresh':refresh_token})

        try:
            serializer.is_valid(raise_exception=True)
        except:
            return Response({'error':'Invalid credentials'},status=status.HTTP_401_UNAUTHORIZED)
            
        access_token = serializer.validated_data['access']
        response = Response({'success':'Token has been successfully refreshed'},status=status.HTTP_200_OK)

        response.set_cookie(
            key='access_token',
            value=access_token,
            httponly=True,
            secure=True,
            samesite='Lax',
            max_age=300
        )
        return  response
    
class CookieTokenObtainView(TokenObtainPairView):
    serializer_class = TokenObtainPairSerializer
    def post(self,request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        try:
            serializer.is_valid(raise_exception=True)
        except:
            return Response({'error':'invalid credentials'},status=status.HTTP_401_UNAUTHORIZED)
        
        access_token = serializer.validated_data['access']
        refresh_token = serializer.validated_data['refresh']

        response = Response({'success':'successfully logged in.'},status=status.HTTP_200_OK)

        response.set_cookie(
            key="access_token",
            value=access_token,
            httponly=True,
            secure=True,
            samesite="Lax",
            max_age=300
        )

        response.set_cookie(
            key="refresh_token",
            value=refresh_token,
            httponly=True,
            secure=False,
            samesite="Lax",
            max_age=60*60*24*7
        )

        return response
  
    
class CustomUserViewSet(ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer
    permission_classes = [CustomUserPermissions]
    filter_backends = [filters.SearchFilter]
    search_fields = ['username','email']
    pagination_class = PageNumberPagination
    pagination_class.page_size = 4
    pagination_class.page_size_query_param = 'size'
    pagination_class.max_page_size = 20

class QuestionsViewSet(ModelViewSet):
    # queryset = Questions.objects.all()
    serializer_class = QuestionsSerializer
    permission_classes = [QuestionPermission]
    filter_backends = [filters.SearchFilter]
    search_fields = ['title','body']
    pagination_class = PageNumberPagination
    pagination_class.page_size = 4
    pagination_class.page_size_query_param = 'size'
    pagination_class.max_page_size = 20

    def get_queryset(self):
        tag_id = self.kwargs.get('tags_pk')
        if tag_id:
            tag = get_object_or_404(Tags,id=tag_id)
            return Questions.objects.filter(tags=tag)
        return Questions.objects.all()

    def perform_create(self, serializer):
        tag_id = self.kwargs.get('tags_pk')
        question = serializer.save(author=self.request.user)
        if tag_id:
            tag = get_object_or_404(Tags,id=tag_id)
            question.tags.add(tag)
        return question


class AnswerViewSet(ModelViewSet):
    serializer_class = AnswerSerializer
    # queryset = Answers.objects.all()
    permission_classes = [AnswerPermission]
    pagination_class = PageNumberPagination
    pagination_class.page_size = 4
    pagination_class.page_size_query_param = 'size'
    pagination_class.max_page_size = 20


    def get_queryset(self):
        question_id = self.kwargs.get('questions_pk')
        print(question_id)
        if question_id:
            question = get_object_or_404(Questions, id=question_id)
            return Answers.objects.filter(question=question)
        return Answers.objects.all()
    
    def perform_create(self, serializer):
        question_id = self.kwargs.get('questions_pk')
        if question_id:
            question = Questions.objects.get(id=question_id)
        else:
            question_id = self.request.POST.get('question')
            question = Questions.objects.get(id=question_id)
        return serializer.save(question=question,author=self.request.user)

    @action(detail=True,methods=['POST'])
    def upvote(self, request,pk=None,questions_pk=None):
        # pk = self.kwargs.get('pk')
        answer = Answers.objects.get(id=pk)
        print(answer.id)
        data = {
            'user':request.user.id,
            'answer':answer.id,
            'value':1
        }

        serializer = VoteSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            print(serializer.data)
            return Response(serializer.data,status=200)
        return Response(serializer.errors)
    
    @action(detail=True,methods=['POST'])
    def downvote(self, request,pk=None,questions_pk=None):
        # pk = self.kwargs.get('pk')
        answer = Answers.objects.get(id=pk)
        print(answer.id)
        data = {
            'user':request.user.id,
            'answer':answer.id,
            'value':-1
        }

        serializer = VoteSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=200)
        return Response(serializer.errors)




class TagViewSet(ModelViewSet):
    # queryset = Tags.objects.all()
    serializer_class = TagSerializer
    permission_classes = [TagsPermission]
    pagination_class = PageNumberPagination
    pagination_class.page_size = 4
    pagination_class.page_size_query_param = 'size'
    pagination_class.max_page_size = 20

    def get_queryset(self):
        question_id = self.kwargs.get('questions_pk')
        if question_id:
            question = get_object_or_404(Questions, id=question_id)
            return Tags.objects.filter(questions=question)
        return Tags.objects.all()
    
    def perform_create(self, serializer):
        question_id = self.kwargs.get('questions_pk')
        tag = serializer.save()
        if question_id:
            question = get_object_or_404(Questions, id=question_id)
            tag.questions.add(question)
        return tag