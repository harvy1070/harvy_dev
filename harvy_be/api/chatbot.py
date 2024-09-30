# chatbot/chatbot.py

from django.utils import timezone
from .models import ChatSession, ChatMessage, UserPreference, PortfolioKeyword, PortfolioFiles
from django.db.models import Q

class Chatbot:
    def __init__(self, user_id=None):
        self.user_id = user_id
        self.session = self._get_or_create_session()

    def _get_or_create_session(self):
        if self.user_id:
            session, created = ChatSession.objects.get_or_create(
                user_id=self.user_id,
                defaults={'session_id': f"session_{self.user_id}_{timezone.now().timestamp()}"}
            )
        else:
            session = ChatSession.objects.create(
                session_id=f"anonymous_{timezone.now().timestamp()}"
            )
        return session

    def process_message(self, message):
        # 사용자 메시지 저장
        ChatMessage.objects.create(session=self.session, is_user=True, message=message)
        
        # 메시지 처리 및 응답 생성
        response = self.generate_response(message)
        
        # 챗봇 응답 저장
        ChatMessage.objects.create(session=self.session, is_user=False, message=response)
        
        # 마지막 상호작용 시간 업데이트
        self.session.last_interaction = timezone.now()
        self.session.save()
        
        return response

    def generate_response(self, message):
        # TODO: 더 정교한 응답 생성 구현 필요
        if '포트폴리오' in message.lower():
            return self.recommend_portfolio(message)
        elif '선호' in message.lower():
            return self.update_preference(message)
        else:
            return "다시 시도해주세요."

    def recommend_portfolio(self, message):
        # 간단한 키워드 기반 포트폴리오 추천
        keywords = message.lower().split()
        portfolios = PortfolioKeyword.objects.filter(keyword__in=keywords).values_list('portfolio', flat=True).distinct()
        
        if portfolios:
            return f"{len(portfolios)}개의 포트폴리오를 찾았습니다."
        else:
            return "해당 키워드와 일치하는 포트폴리오를 찾지 못했습니다. 더 자세히 설명해 주시겠어요?"

    def update_preference(self, message):
        if not self.user_id:
            return "죄송합니다, 선호도를 업데이트하려면 로그인해야 합니다."
        
        # 간단한 선호도 업데이트 로직
        pref, created = UserPreference.objects.get_or_create(user_id=self.user_id)
        
        if '기술' in message.lower():
            pref.pref_tech = message.split('기술')[-1].strip()
        elif '유형' in message.lower():
            pref.pref_pf_types = message.split('유형')[-1].strip()
        
        pref.save()
        return "선호도가 업데이트되었습니다. 더 알고 싶은 것이 있나요?"
