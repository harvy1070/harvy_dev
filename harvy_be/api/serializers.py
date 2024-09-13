from rest_framework import serializers
from .models import *

class UserInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserInfo
        fields = ['user_id', 'user_name', 'user_email', 'user_tel1', 'user_tel2', 'user_addr1', 'user_addr2', 'user_corpname', 'user_corpdept', 'user_corptype', 'user_signin', 'is_active', 'is_staff']
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
    user = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = PortfolioBoard
        fields = ['id', 'user', 'user_name', 'board_title', 'board_desc', 'board_write']
        read_only_fields = ['id', 'board_write']

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