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

# Portfolio
class PortfolioBoardSerializer(serializers.ModelSerializer):
    class Meta:
        model = PortfolioBoard
        fields = ['id', 'board_title', 'board_semidesc', 'board_desc', 'pf_link', 'pf_date', 'order_num'
        ]
        read_only_fields = ['id']

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['pf_date'] = instance.pf_date.strftime('%Y-%m-%d')  # 날짜 형식 지정
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
        fields = ['id', 'type', 'title', 'role', 'company', 'order_company', 'description', 'date', 'order_num']
        read_only_fields = ['id']
        
     
