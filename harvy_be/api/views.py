from rest_framework import viewsets
from .models import *
from .serializers import *
from rest_framework.permissions import IsAuthenticated

class UserInfoViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = UserInfo.objects.all()
    serializer_class = UserInfoSerializer

class QnAViewSet(viewsets.ModelViewSet):
    queryset = QnA.objects.all()
    serializer_class = QnASerializer

class PortfolioBoardViewSet(viewsets.ModelViewSet):
    queryset = PortfolioBoard.objects.all()
    serializer_class = PortfolioBoardSerializer

class PortfolioFilesViewSet(viewsets.ModelViewSet):
    queryset = PortfolioFiles.objects.all()
    serializer_class = PortfolioFilesSerializer

class PjTimelineViewSet(viewsets.ModelViewSet):
    queryset = PjTimeline.objects.all()
    serializer_class = PjTimelineSerializer