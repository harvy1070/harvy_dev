from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.response import Response
from rest_framework.views import APIView  # 이 줄을 추가하세요
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from .serializers import UserInfoSerializer
import logging
from .models import *
from .serializers import *
from rest_framework.permissions import IsAuthenticated
from django.db.models import Prefetch

from django.contrib.auth import get_user_model
from .chatbot import Chatbot

User = get_user_model()
logger = logging.getLogger(__name__)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def check_admin(request):
    # 토큰 확인 작업
    print(f"User: {request.user}, Is superuser: {request.user.is_superuser}")
    return Response({'isAdmin': request.user.is_superuser})

class UserInfoViewSet(viewsets.ModelViewSet):
    queryset = UserInfo.objects.all()
    serializer_class = UserInfoSerializer

    def get_permissions(self):
        if self.action == 'create':
            return [permissions.AllowAny()]
        return [permissions.IsAuthenticated()]

    def get_serializer_class(self):
        if self.action == 'create':
            return UserInfoCreationSerializer
        return UserInfoSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        # user_id 중복 체크
        user_id = serializer.validated_data.get('user_id')
        if UserInfo.objects.filter(user_id=user_id).exists():
            raise serializers.ValidationError({"user_id": "이미 존재하는 사용자 ID입니다."})
        
        user = serializer.save()
        headers = self.get_success_headers(serializer.data)
        return Response(UserInfoSerializer(user).data, status=status.HTTP_201_CREATED, headers=headers)

class AuthViewSet(viewsets.ViewSet):
    @action(detail=False, methods=['post'], permission_classes=[permissions.AllowAny])
    def login(self, request):
        user_id = request.data.get('user_id')
        password = request.data.get('password')
        print(f"Login attempt: user_id={user_id}")
        print(f"Request data: {request.data}")
        try:
            user = User.objects.get(user_id=user_id)
            if user.check_password(password):
                print(f"User authenticated: {user}")
                refresh = RefreshToken.for_user(user)
                return Response({
                    'refresh': str(refresh),
                    'access': str(refresh.access_token),
                    'user': UserInfoSerializer(user).data
                })
            else:
                print(f"Authentication failed for user_id: {user_id}")
                return Response({'error': 'ID/PW를 확인하세요.'}, status=status.HTTP_401_UNAUTHORIZED)
        except User.DoesNotExist:
            print(f"User not found for user_id: {user_id}")
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

    @action(detail=False, methods=['post'], permission_classes=[permissions.IsAuthenticated])
    def logout(self, request):
        try:
            refresh_token = request.data["refresh_token"]
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response(status=status.HTTP_205_RESET_CONTENT)
        except Exception as e:
            return Response(status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['post'])
    def refresh(self, request):
        try:
            refresh_token = request.data["refresh"]
            token = RefreshToken(refresh_token)
            return Response({
                'access': str(token.access_token)
            })
        except Exception as e:
            return Response(status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['get'], permission_classes=[permissions.IsAuthenticated])
    def user(self, request):
        serializer = UserInfoSerializer(request.user)
        return Response(serializer.data)
    
    # 회원가입 view 추가 / 9. 24.
    @action(detail=False, methods=['post'], permission_classes=[permissions.AllowAny])
    def signup(self, request):
        serializer = UserInfoCreationSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            refresh = RefreshToken.for_user(user)
            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
                'user': serializer.data
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class QnAViewSet(viewsets.ModelViewSet):
    queryset = QnA.objects.all().select_related('user')
    serializer_class = QnASerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    # select_related를 사용하여 user 정보를 함께 가져와 쿼리 최적화
    # IsAuthenticatedOrReadOnly를 사용하여 읽기는 모두 가능하지만, 쓰기는 인증된 사용자만 가능하도록 설정

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
    # QnA 생성 시 현재 인증된 사용자를 자동으로 연결

class PortfolioBoardViewSet(viewsets.ModelViewSet):
    queryset = PortfolioBoard.objects.all().select_related('user')
    serializer_class = PortfolioBoardSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def create(self, request, *args, **kwargs):
        logger.info(f"Received data for portfolio creation: {request.data}")
        serializer = self.get_serializer(data=request.data)
        if not serializer.is_valid():
            logger.error(f"Serializer errors: {serializer.errors}")
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        if not serializer.is_valid():
            logger.error(f"Serializer errors in update: {serializer.errors}")
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        self.perform_update(serializer)
        return Response(serializer.data)

    def perform_update(self, serializer):
        serializer.save()

class PortfolioFilesViewSet(viewsets.ModelViewSet):
    queryset = PortfolioFiles.objects.all().select_related('portfolio')
    serializer_class = PortfolioFilesSerializer
    permission_classes = [permissions.IsAuthenticated]

    # select_related를 사용하여 portfolio 정보를 함께 가져와 쿼리 최적화
    # IsAuthenticated를 사용하여 인증된 사용자만 파일을 관리할 수 있도록 설정

    def perform_create(self, serializer):
        serializer.save(portfolio_id=self.request.data.get('portfolio'))
    # 파일 생성 시 연관된 포트폴리오 ID를 자동으로 설정

class PjTimelineViewSet(viewsets.ModelViewSet):
    queryset = PjTimeline.objects.all()
    serializer_class = PjTimelineSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    # IsAuthenticatedOrReadOnly를 사용하여 타임라인 조회는 모두 가능하지만, 수정은 인증된 사용자만 가능하도록 설정

    def get_queryset(self):
        return PjTimeline.objects.all().order_by('order_num', '-date')
    # 타임라인 항목을 order_num과 date 기준으로 정렬하여 반환
    
    
# Chatbot view 추가 // 9. 29. ~
class ChatbotSessionView(APIView):
    def post(self, request):
        # 새로운 챗봇 세션 시작
        user = request.user if request.user.is_authenticated else None
        chatbot = Chatbot(user_id=user.id if user else None)
        serializer = ChatSessionSerializer(chatbot.session)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def delete(self, request, session_id):
        # 챗봇 세션 종료
        try:
            session = ChatSession.objects.get(session_id=session_id)
            session.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except ChatSession.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

class ChatbotMessageView(APIView):
    def post(self, request, session_id):
        # 사용자 메시지 처리 및 챗봇 응답 생성
        try:
            session = ChatSession.objects.get(session_id=session_id)
            chatbot = Chatbot(session_id=session_id)
            user_message = request.data.get('message', '')
            response = chatbot.process_message(user_message)
            return Response({'response': response}, status=status.HTTP_200_OK)
        except ChatSession.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

class PortfolioRecommendationView(APIView):
    def get(self, request, session_id):
        # 포트폴리오 추천
        try:
            session = ChatSession.objects.get(session_id=session_id)
            chatbot = Chatbot(session_id=session_id)
            recommendations = chatbot.recommend_portfolio()
            return Response(recommendations, status=status.HTTP_200_OK)
        except ChatSession.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

class UserPreferenceUpdateView(APIView):
    def put(self, request, user_id):
        # 사용자 선호도 업데이트
        try:
            preference = UserPreference.objects.get(user_id=user_id)
            serializer = UserPreferenceSerializer(preference, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except UserPreference.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)