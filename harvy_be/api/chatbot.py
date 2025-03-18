# chatbot/chatbot.py
from openai import OpenAI
from django.utils import timezone
from django.conf import settings
from .models import *
from django.db.models import Q
from .similarity_utils import is_similar
import os
from django.db.models import Prefetch
import logging
from django.contrib.sessions.models import Session

from django.db.models import Count
try:
    # from konlpy.tag import Okt
    OKT_AVAILABLE = False
except ImportError:
    OKT_AVAILABLE = False
    print("Warning: konlpy module not found. Chatbot functionality will be limited.")
# from konlpy.tag import Okt
import traceback
from django.http import JsonResponse

client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

# 입출력값 조절
MAX_INPUT_LEN = 500
MAX_OUTPUT_LEN = 1000
MAX_TOKENS = 500

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

class Chatbot:
    def __init__(self, request):
        self.request = request
        self.user = request.user if request.user.is_authenticated else None
        logger.debug(f"사용자 초기화 중: {self.user}")
        self.session = self._get_or_create_session()
        # konlpy가 있을 때만 Okt 초기화
        if OKT_AVAILABLE:
            self.okt = Okt()
        else:
            self.okt = None
        self.stop_words = self.load_stop_words()
        self.conversation_history = []

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

    def load_stop_words(self):
        base_dir = settings.BASE_DIR
        sw_path = os.path.join(base_dir, 'pdf_files', 'stopword.txt')
        with open(sw_path, 'r', encoding='utf-8') as f:
            return set(line.strip() for line in f)

    def process_message(self, message):
        logger.debug(f"process_message 시작: message = {message}")
        try:
            if len(message) > MAX_INPUT_LEN:
                logger.debug(f"메시지 길이 초과: {len(message)} > {MAX_INPUT_LEN}")
                return f"입력은 {MAX_INPUT_LEN}자를 초과할 수 없습니다."
            
            logger.debug(f"받은 메시지: {message}")
            logger.debug(f"현재 대화 기록: {self.conversation_history}")
            
            chat_message = ChatMessage.objects.create(
                user=self.user,
                user_message=message
            )
            logger.debug(f"ChatMessage 생성됨: {chat_message}")
            
            self.conversation_history.append(message)
            logger.debug(f"대화 기록 업데이트: {self.conversation_history}")
            
            recommended_portfolios = []
            if len(self.conversation_history) >= 3:
                logger.debug("3회 대화 완료, 포트폴리오 추천 시작")
                recommended_portfolios = self.recommend_portfolio()
                logger.debug(f"추천된 포트폴리오: {recommended_portfolios}")
                self.conversation_history = []  # 대화 기록 초기화
                logger.debug("대화 기록 초기화됨")
            
            logger.debug("GPT 응답 생성 시작")
            gpt_response = self.generate_gpt_response(message, recommended_portfolios)
            logger.debug(f"GPT 응답 생성 완료: {gpt_response}")
            
            if gpt_response is None:
                gpt_response = "응답 생성 중 오류가 발생했습니다."
            
            chat_message.gpt_message = gpt_response
            chat_message.save()
            logger.debug("ChatMessage에 GPT 응답 저장됨")

            logger.debug(f"process_message 종료: 반환값 = {gpt_response}")
            return {"response": gpt_response}
        except Exception as e:
            logger.error(f"메시지 처리 중 오류 발생: {e}")
            logger.error(traceback.format_exc())  # 상세한 오류 트레이스백 출력
            return "메시지 처리 중 오류가 발생했습니다. 다시 시도해 주세요."

    def generate_gpt_response(self, message, recommended_portfolios):
        logger.debug(f"generate_gpt_response 시작: message = {message}, recommended_portfolios = {recommended_portfolios}")
        try:
            conv_history = self.get_conv_history()
            logger.debug(f"대화 기록: {conv_history}")
            
            try:
                pf_info = self.format_portfolio_recommendations(recommended_portfolios)
                logger.debug(f"포맷된 포트폴리오 정보: {pf_info}")
            except Exception as e:
                logger.error(f"포트폴리오 추천 정보 포맷 중 오류 발생: {str(e)}")
                pf_info = "포트폴리오 추천 정보를 가져오는 데 문제가 발생했습니다."
            
            prompt = f"이전 대화 내용입니다. \n{conv_history}\n\n사용자: {message}\n\n"
            if recommended_portfolios:
                prompt += f"추천 포트폴리오 정보:\n{pf_info}\n\n"
            prompt += "위 정보를 바탕으로 답변합니다."
            
            logger.debug(f"GPT에 전송되는 프롬프트: {prompt}")
            
            try:
                response = client.chat.completions.create(
                    model="gpt-3.5-turbo",
                    messages=[{"role": "system", "content": prompt}],
                    max_tokens=MAX_TOKENS
                )
                gpt_response = response.choices[0].message.content.strip()
                logger.debug(f"GPT 원본 응답: {gpt_response}")

                if len(gpt_response) > MAX_OUTPUT_LEN:
                    gpt_response = gpt_response[:MAX_OUTPUT_LEN] + "..."
                    logger.debug(f"GPT 응답 길이 조정됨: {gpt_response}")
                
                logger.debug(f"generate_gpt_response 종료: 반환값 = {gpt_response}")
                return gpt_response
            except Exception as e:
                logger.error(f"OpenAI API 호출 중 오류 발생: {str(e)}")
                return "OpenAI API 호출 중 오류가 발생했습니다."
        except Exception as e:
            logger.error(f"generate_gpt_response 전체 오류: {str(e)}")
            return "응답 생성 중 오류가 발생했습니다."
    
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
    
    # 대화내용에서 Keyword 추출
    def extract_keywords(self, text):
        if self.okt is None:
            # konlpy 없을 때 대체 구현 - 단순 공백 기준 분리
            words = text.split()
            return [word for word in words if word not in self.stop_words]
        else:
            # 기존 구현
            nouns = self.okt.nouns(text)
            return [word for word in nouns if word not in self.stop_words]
    
    def calc_pf_scores(self, keywords):
        return PortfolioKeyword.objects.filter(keyword__in=keywords).values('portfolio').annotate(score=Count('keyword')).order_by('-score')
        
    def get_top(self, pf_scores, limit=3):
        top_pf = []
        for score in pf_scores[:limit]:
            pf = PortfolioBoard.objects.get(id=score['portfolio'])
            top_pf.append({
                'id': pf.id,
                'title': pf.board_title,
                'desc': pf.board_semidesc,
                'score': score['score']
            })
        return top_pf
        
    # 최근 대화내용 불러오기
    def recommend_portfolio(self):
        try:
            conversation = ' '.join(self.conversation_history)
            logger.debug(f"추천을 위한 대화 내용: {conversation}")
            keywords = self.extract_keywords(conversation)
            logger.debug(f"추출된 키워드: {keywords}")
            
            portfolio_keywords = PortfolioKeyword.objects.filter(keyword__in=keywords)
            portfolio_scores = {}
            
            for pk in portfolio_keywords:
                if pk.portfolio_id in portfolio_scores:
                    portfolio_scores[pk.portfolio_id] += 1
                else:
                    portfolio_scores[pk.portfolio_id] = 1
            
            sorted_portfolios = sorted(portfolio_scores.items(), key=lambda x: x[1], reverse=True)
            top_portfolios = sorted_portfolios[:3]
            
            recommended_portfolios = []
            for portfolio_id, score in top_portfolios:
                try:
                    portfolio = PortfolioBoard.objects.get(id=portfolio_id)
                    recommended_portfolios.append({
                        'id': portfolio.id,
                        'title': portfolio.board_title,
                        'description': portfolio.board_semidesc,
                        'score': score
                    })
                except PortfolioBoard.DoesNotExist:
                    logger.error(f"포트폴리오 ID {portfolio_id}를 찾을 수 없습니다.")
            
            logger.debug(f"추천된 포트폴리오: {recommended_portfolios}")
            return recommended_portfolios
        except Exception as e:
            logger.error(f"포트폴리오 추천 중 오류 발생: {str(e)}")
            return []

    def generate_gpt_response(self, message, recommended_portfolios):
        try:
            conv_history = self.get_conv_history()
            try:
                pf_info = self.format_portfolio_recommendations(recommended_portfolios)
            except Exception as e:
                logger.error(f"포트폴리오 추천 정보 포맷 중 오류 발생: {str(e)}")
                pf_info = "포트폴리오 추천 정보를 가져오는 데 문제가 발생했습니다."
            
            prompt = f"이전 대화 내용입니다. \n{conv_history}\n\n사용자: {message}\n\n"
            if recommended_portfolios:
                prompt += f"추천 포트폴리오 정보:\n{pf_info}\n\n"
            prompt += "위 정보를 바탕으로 답변합니다."
            
            # 나머지 코드는 그대로 유지
        except Exception as e:
            logger.error(f"OpenAI API 오류: {str(e)}")
            return "현재 응답을 생성하는 데 오류가 생겼습니다. 관리자에게 문의 바랍니다."
    
    def format_portfolio_recommendations(self, portfolios):
        if not portfolios:
            return "관련 포트폴리오를 찾지 못했습니다."
        
        info = "추천 포트폴리오:\n"
        for pf in portfolios:
            info += f"- {pf['title']} (점수: {pf['score']}): {pf['description'][:100]}...\n"
        return info
            
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
