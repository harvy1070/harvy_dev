from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin

# 사용자 생성 로직 관리(일반유저, super유저 구분)
class UserInfoManager(BaseUserManager):
    def create_user(self, user_id, user_email, user_name, password, **extra_fields):
        if not user_id:
            raise ValueError('사용자 ID 필드를 설정해야 합니다.')
        if not user_email:
            raise ValueError('Email 필드를 설정해야 합니다.')
        email = self.normalize_email(user_email)
        user = self.model(user_id=user_id, user_email=email, user_name=user_name, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, user_id, user_email, user_name, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(user_id, user_email, user_name, password, **extra_fields)
    
# 유저정보 모델 정의
class UserInfo(AbstractBaseUser, PermissionsMixin):
    user_id = models.CharField(max_length=20, primary_key=True, unique=True, verbose_name='ID')
    user_name = models.CharField(max_length=20, verbose_name='유저이름')
    user_email = models.EmailField(unique=True, verbose_name='이메일')
    user_tel2 = models.CharField(max_length=20, verbose_name='무선번호(핸드폰)')
    user_corpname = models.CharField(max_length=20, verbose_name='소속회사')
    user_corpdept = models.CharField(max_length=20, verbose_name='소속부서')
    user_signin = models.DateTimeField(auto_now_add=True, verbose_name='가입일')
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserInfoManager()

    USERNAME_FIELD = 'user_id'  # 로그인에 사용될 필드를 'user_id'로 설정
    REQUIRED_FIELDS = ['user_email', 'user_name'] # createsuperuser를 위한 필드

    def __str__(self):
        return self.user_email

    class Meta:
        db_table = 'userinfo'
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

    class Meta:
        db_table = 'qna'

    def __str__(self):
        return self.question_title

# Portfolio 게시판 모델 정의
# migrate를 위해 우선적으로 null값을 넣어두고 추후 데이터를 추가시 null해제
class PortfolioBoard(models.Model):
    pf_type_choice = [
        ('AI', 'AI'),
        ('Planning', '기획'),
        ('WEB_DEV', '웹 개발'),
    ]
    user = models.ForeignKey(UserInfo, on_delete=models.CASCADE, related_name='portfolios', null=True)
    board_title = models.CharField(max_length=200, verbose_name='프로젝트 제목', null=True)
    board_semidesc = models.TextField(verbose_name='프로젝트 간단 설명', null=True)
    desc_role = models.TextField(verbose_name='역할', null=True)
    desc_info = models.TextField(verbose_name='프로젝트 소개', null=True)
    desc_tasks = models.TextField(verbose_name='주요 작업 내역', null=True)
    desc_results = models.TextField(verbose_name='결과', null=True)
    pf_link = models.URLField(null=True, blank=True, verbose_name='프로젝트 링크')
    pf_start_date = models.DateField(verbose_name='프로젝트 시작일', null=True)
    pf_end_date = models.DateField(verbose_name='프로젝트 종료일', null=True, blank=True)  # 진행 중인 프로젝트를 위해 null 허용
    order_num = models.IntegerField(blank=True, null=True, verbose_name='표시 순서')
    pf_type = models.CharField(max_length=20, choices=pf_type_choice, verbose_name='포트폴리오 유형', default='AI')

    class Meta:
        db_table = 'portfolioboard'
        
    @property
    def project_period(self):
        if self.pf_end_date:
            return f"{self.pf_start_date.strftime('%Y. %m. %d.')} ~ {self.pf_end_date.strftime('%Y. %m. %d.')}"
        return f"{self.pf_start_date.strftime('%Y. %m. %d.')} ~ 진행 중"

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

    class Meta:
        db_table = 'portfoliofiles'

    def __str__(self):
        return self.file_name

# 개인 연혁 관련 모델 정의 
class PjTimeline(models.Model):
    # TYPE_CHOICES = (
    #     ('career', '경력'),
    #     ('project', '프로젝트'),
    # )
    # type = models.CharField(max_length=20, choices=TYPE_CHOICES, verbose_name='항목 유형')
    title = models.CharField(max_length=100, verbose_name='프로젝트 명')
    role = models.CharField(max_length=100, blank=True, null=True, verbose_name='참여 역할')
    company = models.CharField(max_length=100, blank=True, null=True, verbose_name='소속 회사')
    order_company = models.CharField(max_length=100, blank=True, null=True, verbose_name='발주처') 
    description = models.TextField(blank=True, null=True, verbose_name='설명')
    date = models.DateField(verbose_name='날짜')
    order_num = models.IntegerField(blank=True, null=True, verbose_name='표시 순서')

    class Meta:
        db_table = 'pjtimeline'
        ordering = ['order_num', '-date']

    def __str__(self):
        return f"{self.title} ({self.date})"