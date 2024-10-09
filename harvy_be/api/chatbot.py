# chatbot/chatbot.py
import openai
from django.utils import timezone
from django.conf import settings
from .models import *
from django.db.models import Q
from .similarity_utils import is_similar
import os
from django.db.models import Prefetch
import logging
from django.contrib.sessions.models import Session

openai.api_key = os.getenv('OPENAI_API_KEY')

# 입출력값 조절
MAX_INPUT_LEN = 500
MAX_OUTPUT_LEN = 1000
MAX_TOKENS = 500

logger = logging.getLogger(__name__)

class Chatbot:
    def __init__(self, request):
        self.request = request
        self.user = request.user if request.user.is_authenticated else None
        logger.debug(f"사용자 초기화 중: {self.user}")
        self.session = self._get_or_create_session()

    def _get_or_create_session(self):
        try:
            if not self.request.session.session_key:
                self.request.session.create()
            
            session_key = self.request.session.session_key
            
            # Django Session 객체 가져오기 또는 생성
            django_session = Session.objects.get(session_key=session_key)
            
            # ChatSession 객체 가져오기 또는 생성
            chat_session, created = ChatSession.objects.get_or_create(
                session_key=session_key,
                defaults={'user': self.user}
            )
            
            return chat_session
        except Session.DoesNotExist:
            # 세션이 존재하지 않는 경우 새로 생성
            self.request.session.create()
            session_key = self.request.session.session_key
            django_session = Session.objects.get(session_key=session_key)
            chat_session = ChatSession.objects.create(session_key=session_key, user=self.user)
            return chat_session
        except Exception as e:
            logger.error(f"Error in _get_or_create_session: {str(e)}", exc_info=True)
            raise

    def process_message(self, message):
        try:
            if len(message) > MAX_INPUT_LEN:
                return f"입력은 {MAX_INPUT_LEN}자를 초과할 수 없습니다."
            
            chat_message = ChatMessage.objects.create(
                user=self.user,
                user_message=message
            )
            
            gpt_response = self.generate_gpt_response(message)
            
            chat_message.gpt_message = gpt_response
            chat_message.save()

            return gpt_response
        except Exception as e:
            print(f"메시지 처리 중 오류 발생: {e}")
            return "메시지 처리 중 오류가 발생했습니다. 다시 시도해 주세요."

    def generate_gpt_response(self, message):
        try:
            conv_history = self.get_conv_history()
            pf_info = self.get_pf_recommendations(message)
            
            prompt = f"이전 대화 내용입니다. \n{conv_history}\n\n사용자: {message}\n\n추천 포트폴리오 정보:\n{pf_info}\n\n 위 정보를 바탕으로 답변합니다."
        
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "system", "content": prompt}],
                max_tokens=MAX_TOKENS
            )
            gpt_response = response.choices[0].message['content'].strip()

            if len(gpt_response) > MAX_OUTPUT_LEN:
                gpt_response = gpt_response[:MAX_OUTPUT_LEN] + "..."
            
            return gpt_response
        except Exception as e:
            print(f"OpenAI API 오류: {e}")
            return "현재 응답을 생성하는 데 오류가 생겼습니다. 관리자에게 문의 바랍니다."
            
    def get_conv_history(self):
        if self.user:
            recent_messages = ChatMessage.objects.filter(user=self.user).order_by('-id')[:5]
        else:
            session_key = self.request.session.session_key
            if not session_key:
                self.request.session.create()
                session_key = self.request.session.session_key
            recent_messages = ChatMessage.objects.filter(session_key=session_key).order_by('-id')[:5]
            
        history = ""
        for m in reversed(recent_messages):
            if m.user_message:
                history += f"사용자: {m.user_message}\n"
            if m.gpt_message:
                history += f"챗봇: {m.gpt_message}\n"
        return history
        
    # 최근 대화내용 불러오기
    def recommend_portfolio(self):
        conversation = self.get_conv_history()
        
        user_pref = None
        if self.user:
            user_pref = UserPreference.objects.filter(user=self.user).first()
        
        # 추천 로직
        recommend_pf = []
        portfolios = PortfolioBoard.objects.prefetch_related(
            Prefetch('keywords', queryset=PortfolioKeyword.objects.all(), to_attr='prefetched_keywords')
        )
        
        for pf in portfolios:
            pf_keywords = " ".join([kw.keyword for kw in pf.prefetched_keywords])
            
            # 대화 내용과의 유사도 계산
            is_similar_conv, similarity_score = is_similar(conversation, pf_keywords, threshold=0.3)
            
            score = similarity_score
            
            # 선호도 반영
            if user_pref:
                if pf.pf_type in user_pref.pref_pf_types.split(','):
                    score += 0.2
                pref_techs = user_pref.pref_tech.split(',')
                if any(tech.strip().lower() in pf_keywords.lower() for tech in pref_techs):
                    score += 0.1
            
            if score > 0:
                recommend_pf.append((pf, score))
        
        # 점수에 따라 정렬
        recommend_pf.sort(key=lambda x: x[1], reverse=True)

        # 상위 3개 포트폴리오 반환
        top_recommendations = recommend_pf[:3]
        
        if top_recommendations:
            recommendations = []
            for pf, score in top_recommendations:
                recommendations.append({
                    'id': pf.id,
                    'title': pf.board_title,
                    'description': pf.board_semidesc,
                    'score': round(score, 2)
                })
            return recommendations
        else:
            return []
            
    # 포트폴리오 추천 정보 및 유사도 측정
    def get_pf_recommendations(self, message):
        recommended_portfolios = self.recommend_portfolio()
        
        if recommended_portfolios:
            info = "추천 포트폴리오\n"
            for pf in recommended_portfolios:
                info += f"- {pf['title']} (점수: {pf['score']})\n"
            return info
        else:
            return "관련 포트폴리오를 찾지 못했습니다."
    
    def update_preference(self, message):
        if not self.user:
            return "죄송합니다, 선호도를 업데이트하려면 로그인해야 합니다."
        
        # 선호도 업데이트
        pref, created = UserPreference.objects.get_or_create(user=self.user)
        
        if '기술' in message.lower():
            pref.pref_tech = message.split('기술')[-1].strip()
        elif '유형' in message.lower():
            pref.pref_pf_types = message.split('유형')[-1].strip()
        
        pref.save()
        return "선호도가 업데이트되었습니다. 더 알고 싶은 것이 있나요?"
