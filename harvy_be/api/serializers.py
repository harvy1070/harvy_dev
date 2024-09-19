from rest_framework import serializers
from .models import *

class UserInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserInfo
        fields = ['user_id', 'user_name', 'user_email', 'user_tel2', 'user_corpname', 'user_corpdept', 'user_signin', 'is_active', 'is_staff']
        # 읽기전용 필드 설정
        read_only_fields = ['user_id', 'user_signin']
        # Password필드는 쓰기 전용으로 설정
        extra_kwargs = {
            # 응답에 포함되지 않도록 함
            'password': {'write_only': True}
        }
        
    # 새 UserInfo 생성
    def create(self, validated_data):
        # UserInfo에서 제공하는 create_user 메서드를 사용하여 생성
        return UserInfo.objects.create_user(**validated_data)
    
    # 기존 UserInfo 업데이트
    def update(self, instance, validated_data):
        # password 필드가 요청 데이터에 포함되어 있다면 비밀번호 설정
        if 'password' in validated_data:
            password = validated_data.pop('password')
            instance.set_password(password) # django 암호화 기능 사용
        # update 메서드 호출하여 나머지 업데이트 
        return super().update(instance, validated_data)

# 가입 관련
class UserInfoCreationSerializer(serializers.ModelSerializer):
    user_id = serializers.CharField(max_length=20)
    password1 = serializers.CharField(write_only=True)
    password2 = serializers.CharField(write_only=True)

    class Meta:
        model = UserInfo
        fields = ('user_id', 'user_email', 'user_name', 'password1', 'password2', 'user_tel2',
                  'user_corpname', 'user_corpdept')
        
    # 아이디 중복 검증
    def validate_user_id(self, value):
        if UserInfo.objects.filter(user_id=value).exists():
            raise serializers.ValidationError("이미 사용 중인 아이디입니다.")
        return value

    # Password 확인 절차
    def validate(self, data):
        if data['password1'] != data['password2']:
            raise serializers.ValidationError("비밀번호가 일치하지 않습니다.")
        return data

    # 비밀번호 확인을 마친 데이터로 새로운 유저 생성
    def create(self, validated_data):
        user = UserInfo.objects.create_user(
            user_id=validated_data['user_id'],
            user_email=validated_data['user_email'],
            user_name=validated_data['user_name'],
            password=validated_data['password1'],
            **{k: v for k, v in validated_data.items() if k not in ['user_id', 'user_email', 'user_name', 'password1', 'password2']}
        )
        return user

# QnA
class QnASerializer(serializers.ModelSerializer):
    # Pk를 사용하여 정보 저장(읽기 전용)
    user = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = QnA
        fields = ['id', 'user', 'question_title', 'question_desc', 'created_at', 'answer_title', 'answer_desc', 'answered_at']
        read_only_fields = ['id', 'created_at', 'answered_at']

# Portfolio / 9. 16. type 추가(AI, 기획, 웹 개발)
# 9. 16. 추가 수정(가시성 개선을 위한 모델 증축)
class PortfolioBoardSerializer(serializers.ModelSerializer):
    class Meta:
        model = PortfolioBoard
        fields = [
            'id', 
            'user',           # ForeignKey 관련 필드는 모델에서 `user`로 정의됨.
            'pf_type',        # 포트폴리오 유형
            'board_title',    # 프로젝트 제목
            'board_semidesc', # 프로젝트 간단 설명
            'desc_role',      # 역할
            'desc_info',      # 프로젝트 소개
            'desc_tasks',     # 주요 작업 내역
            'desc_results',   # 결과
            'pf_link',        # 프로젝트 링크
            'pf_start_date',  # 프로젝트 시작일
            'pf_end_date',    # 프로젝트 종료일
            'order_num',       # 표시 순서
            'project_period',  # 시작 + 종료일
        ]
        read_only_fields = ['id', 'user', 'project_period']

    def validate(self, data):
        if 'pf_start_date' in data and 'pf_end_date' in data:
            if data['pf_end_date'] and data['pf_start_date'] > data['pf_end_date']:
                raise serializers.ValidationError("종료일은 시작일보다 늦어야 합니다.")
        return data

    def get_project_period(self, obj):
        if obj.pf_start_date:
            start = obj.pf_start_date.strftime('%Y. %m. %d.')
            if obj.pf_end_date:
                end = obj.pf_end_date.strftime('%Y. %m. %d.')
                return f"{start} ~ {end}"
            return f"{start} ~ 진행 중"
        return None

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['pf_start_date'] = instance.pf_start_date.strftime('%Y-%m-%d') if instance.pf_start_date else None
        representation['pf_end_date'] = instance.pf_end_date.strftime('%Y-%m-%d') if instance.pf_end_date else None
        return representation

# Pf의 File 관리
class PortfolioFilesSerializer(serializers.ModelSerializer):
    class Meta:
        model = PortfolioFiles
        fields = ['id', 'portfolio', 'file_name', 'file_path', 'file_size', 'file_type', 'upload_date']
        read_only_fields = ['id', 'upload_date']

# 프로젝트 연혁 관리
class PjTimelineSerializer(serializers.ModelSerializer):
    class Meta:
        model = PjTimeline
        fields = ['id', 'title', 'role', 'company', 'order_company', 'description', 'date', 'order_num']
        read_only_fields = ['id']
        
     
