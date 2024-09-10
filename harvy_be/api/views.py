from rest_framework import viewsets, permissions
from .models import *
from .serializers import *
from rest_framework.permissions import IsAuthenticated
from django.db.models import Prefetch

class UserInfoViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = UserInfo.objects.all()
    serializer_class = UserInfoSerializer

    # IsAuthenticated를 사용하여 인증된 사용자만 접근 가능하도록 설정
    # 사용자 정보는 민감할 수 있으므로 보안 강화

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
    # 새 UserInfo 객체 생성 시 현재 인증된 사용자와 연결

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