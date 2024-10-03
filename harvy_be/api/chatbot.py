# chatbot/chatbot.py
import openai
from django.utils import timezone
from django.conf import settings
from .models import *
from django.db.models import Q
from .similarity_utils import is_similar
import os

openai.api_key = os.getenv('OPENAI_API_KEY')

# 입출력값 조절
MAX_INPUT_LEN = 500
MAX_OUTPUT_LEN = 1000
MAX_TOKENS = 150

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
        if len(message) > MAX_INPUT_LEN:
            return f"입력은 {MAX_INPUT_LEN}자를 초과할 수 없습니다."
        
        # user 메시지 저장
        ChatMessage.objects.create(session=self.session, is_user=True, message=message)
        
        # gpt 응답 생성
        response = self.generate_gpt_response(message)
        
        # 응답 DB에 저장
        ChatMessage.objects.create(session=self.session, is_user=False, message=response)
        
        # 상호작용 시간 업데이트
        self.session.last_interaction = timezone.now()
        self.session.save()

    def generate_gpt_response(self, message):
        try:
            # 이전 대화 내용 가져오기
            conv_history = self.get_conv_history()
            
            # 포트폴리오 추천 정보 가져오기
            pf_info = self.get_pf_recommendations(message)
            
            # GPT에 전달할 프롬프트
            prompt = f"이전 대화 내용입니다. \n{conv_history}\n\n사용자: {message}\n\n추천 포트폴리오 정보:\n{pf_info}\n\n 위 정보를 바탕으로 답변합니다."
        
            # GPT API 호출
            response = openai.ChatCompletion.create(
                model = "gpt-3.5-turbo",
                messages = [{"role": "system", "content":prompt}],
                max_tokens = MAX_TOKENS
            )
            # 생성된 응답 받기
            gpt_response = response.choices[0].message['content'].strip()

            # 길이 제한(gpt 응답 값)
            if len(gpt_response) > MAX_OUTPUT_LEN:
                gpt_response = gpt_response[:MAX_OUTPUT_LEN] + "..."
            
            return gpt_response
        except Exception as e:
            print(f"Open API 오류: {e}")
            return "현재 응답을 생성하는 데 오류가 생겼습니다. 관리자에게 문의 바랍니다."
            
    def get_conv_history(self):
        # 최근 5개 메시지 가져오기
        recent_messages = ChatMessage.objects.filter(session=self.session).order_by('-id')[:5]
        history = ""
        for m in reversed(recent_messages):
            role = "사용자" if m.is_user else "챗봇"
            history += f"{role}: {m.message}\n"
        return history
            
    # 포트폴리오 추천 정보 및 유사도 측정
    def get_pf_recommendations(self, message):
        similar_pf = []
        for pf in PortfolioBoard.objects.all():
            pf_keywords = " ".join(PortfolioKeyword.objects.filter(pf=pf).values_list('keyword', flat=True))
            is_similar_bool, similarity_score = is_similar(message, pf_keywords)
            if is_similar_bool:
                similar_pf.append((pf, similarity_score))
                
        similar_pf.sort(key=lambda x: x[1], reverse=True)
        
        if similar_pf:
            info = "추천 포트폴리오\n"
            for pf, score in similar_pf[:3]:
                info += f"- {pf.board_title}\n"
            return info
        
        else:return "관련 포트폴리오를 찾지 못했습니다."
    
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
