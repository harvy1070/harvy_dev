from rest_framework import viewsets, permissions, status, serializers
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from .serializers import UserInfoSerializer

from .models import *
from .serializers import *
from rest_framework.permissions import IsAuthenticated
from django.db.models import Prefetch

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
        user_id = request.data.get('user_id')  # user_email 대신 user_id 사용
        password = request.data.get('password')
        user = authenticate(username=user_id, password=password)  # username 파라미터에 user_id 사용
        if user:
            refresh = RefreshToken.for_user(user)
            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
                'user': UserInfoSerializer(user).data
            })
        return Response({'error': 'Invalid Credentials'}, status=status.HTTP_401_UNAUTHORIZED)

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

    # select_related를 사용하여 user 정보를 함께 가져와 쿼리 최적화
    # IsAuthenticatedOrReadOnly를 사용하여 포트폴리오 조회는 모두 가능하지만, 수정은 인증된 사용자만 가능하도록 설정

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
    # 포트폴리오 생성 시 현재 인증된 사용자를 자동으로 연결

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