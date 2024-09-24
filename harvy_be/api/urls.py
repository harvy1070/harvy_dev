from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import *
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

# CRUD 작업을 위한 ViewSet 등록, Router
router = DefaultRouter()

# URL 패턴 등록
# ex) r'users' = /users/
router.register(r'users', UserInfoViewSet)
router.register(r'auth', AuthViewSet, basename='auth')
router.register(r'qna', QnAViewSet)
router.register(r'portfolios', PortfolioBoardViewSet)
router.register(r'portfolio-files', PortfolioFilesViewSet)
router.register(r'timeline', PjTimelineViewSet)

# 패턴 목록 정의
urlpatterns = [
    path('', include(router.urls)),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('check-admin/', check_admin, name='check-admin'),
    path('signup/', AuthViewSet.as_view({'post': 'signup'}), name='signup'),
]