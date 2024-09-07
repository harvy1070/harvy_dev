from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin

# 사용자 생성 로직 관리(일반유저, super유저 구분)
class UserInfoManager(BaseUserManager):
    def create_user(self, user_email, user_name, user_pw, **extra_fields):
        if not user_email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(user_email)
        user = self.model(user_email=email, user_name=user_name, **extra_fields)
        user.set_password(user_pw)
        user.save(using=self._db)
        return user

    def create_superuser(self, user_email, user_name, user_pw, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        return self.create_user(user_email, user_name, user_pw, **extra_fields)

# 유저정보 모델 정의
class UserInfo(AbstractBaseUser, PermissionsMixin):
    user_id = models.AutoField(primary_key=True, verbose_name='ID')
    user_name = models.CharField(max_length=20, verbose_name='유저이름')
    user_email = models.EmailField(unique=True, verbose_name='이메일')
    user_tel1 = models.CharField(max_length=20, blank=True, null=True, verbose_name='유선번호')
    user_tel2 = models.CharField(max_length=20, verbose_name='무선번호(핸드폰)')
    user_addr1 = models.CharField(max_length=50, blank=True, null=True, verbose_name='주소')
    user_addr2 = models.CharField(max_length=50, blank=True, null=True, verbose_name='세부주소')
    user_corpname = models.CharField(max_length=20, verbose_name='소속회사')
    user_corpdept = models.CharField(max_length=20, verbose_name='소속부서')
    user_corptype = models.CharField(max_length=20, verbose_name='회사유형')
    user_signin = models.DateTimeField(auto_now_add=True, verbose_name='가입일')
    
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserInfoManager()

    USERNAME_FIELD = 'user_email'
    REQUIRED_FIELDS = ['user_name']

    def __str__(self):
        return self.user_email

    class Meta:
        verbose_name = '사용자'
        verbose_name_plural = '사용자들'

# QnA 게시판 모델 정의
class QnA(models.Model):
    user = models.ForeignKey(UserInfo, on_delete=models.CASCADE, related_name='qnas')
    question_title = models.TextField(verbose_name='질문 제목')
    question_desc = models.TextField(verbose_name='질문 내용')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='질문 작성일')
    answer_title = models.TextField(blank=True, null=True, verbose_name='답변 제목')
    answer_desc = models.TextField(blank=True, null=True, verbose_name='답변 내용')
    answered_at = models.DateTimeField(blank=True, null=True, verbose_name='답변 작성일')

    def __str__(self):
        return self.question_title

# Portfolio 게시판 모델 정의
class PortfolioBoard(models.Model):
    user = models.ForeignKey(UserInfo, on_delete=models.CASCADE, related_name='portfolios')
    user_name = models.CharField(max_length=20, verbose_name='유저이름')
    board_title = models.TextField(verbose_name='글 제목')
    board_desc = models.TextField(blank=True, null=True, verbose_name='글 내용')
    board_write = models.DateTimeField(auto_now_add=True, verbose_name='글 작성일')

    def __str__(self):
        return self.board_title

# Portfolio 게시판에 올리는 파일 관리하는 모델 정의
class PortfolioFiles(models.Model):
    portfolio = models.ForeignKey(PortfolioBoard, on_delete=models.CASCADE, related_name='files')
    file_name = models.CharField(max_length=255, verbose_name='업로드된 파일 이름')
    file_path = models.CharField(max_length=255, verbose_name='파일 저장 경로')
    file_size = models.IntegerField(blank=True, null=True, verbose_name='파일 크기 (바이트)')
    file_type = models.CharField(max_length=50, blank=True, null=True, verbose_name='파일 MIME 타입')
    upload_date = models.DateTimeField(auto_now_add=True, verbose_name='파일 업로드 일시')

    def __str__(self):
        return self.file_name

# 개인 연혁 관련 모델 정의 
class PjTimeline(models.Model):
    TYPE_CHOICES = (
        ('career', '경력'),
        ('project', '프로젝트'),
    )
    type = models.CharField(max_length=20, choices=TYPE_CHOICES, verbose_name='항목 유형')
    title = models.CharField(max_length=100, verbose_name='프로젝트 명')
    description = models.TextField(blank=True, null=True, verbose_name='설명')
    date = models.DateField(verbose_name='날짜')
    order_num = models.IntegerField(blank=True, null=True, verbose_name='표시 순서')

    class Meta:
        ordering = ['order_num', '-date']

    def __str__(self):
        return f"{self.get_type_display()}: {self.title} ({self.date})"