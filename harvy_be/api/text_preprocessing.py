import os, re, sys, django
from collections import Counter
from django.conf import settings

# 프로젝트 루트 디렉토리를 Python 경로에 추가
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(project_root)

# Django 설정 초기화
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "harvy_portfolio.settings_dev")
django.setup()

from django.db import transaction
from api.models import PortfolioBoard, PortfolioKeyword

# 불용어 목록 읽어와서 set으로 변환
def load_stopwords(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return set(word.strip() for word in file)

# 텍스트 전처리
def preprocess_text(text):
    text = re.sub(r'\n+', '\n', text)
    text = re.sub(r'\s+', ' ', text)
    return text.strip()

# 키워드 추출
def extract_keywords(text, stopwords):
    # 코드 블록을 찾아 별도로 처리
    code_blocks = re.findall(r'```[\s\S]*?```', text)
    for i, block in enumerate(code_blocks):
        text = text.replace(block, f'CODE_BLOCK_{i}')
    
    # 일반 텍스트에서 단어 추출
    words = re.findall(r'\b[\w가-힣]+\b', text)
    
    # 코드 블록에서 키워드 추출
    code_words = []
    for block in code_blocks:
        code_words.extend(re.findall(r'\b[\w]+\b', block))
    
    # 불용어 및 짧은 단어 제거 (코드 키워드는 제외)
    words = [word for word in words if word.lower() not in stopwords and len(word) > 1]
    words.extend(code_words)
    
    # 상위 50개 설정
    # return Counter(words).most_common(50)  # 상위 50개 키워드로 증가

    # 전체 키워드 반환
    return Counter(words).items()

# .txt 순차적으로 처리
def process_txt_files(folder_path, stopwords):
    for filename in os.listdir(folder_path):
        if filename.endswith('.txt') and not filename.startswith('processed_'):
            file_path = os.path.join(folder_path, filename)
            print(f"{filename} 파일을 처리 중...")
            
            with open(file_path, 'r', encoding='utf-8') as file:
                text = file.read()
            
            processed_text = preprocess_text(text)
            keywords = extract_keywords(processed_text, stopwords)
            
            # 정상적으로 추출되는지 테스트
            # print(f"Top 20 keywords for {filename}:")
            # for keyword, frequency in keywords:
            #     print(f"{keyword}: {frequency}")
            
            # 테스트 후 해제(저장)
            portfolio_title = os.path.splitext(filename)[0]
            save_to_database(portfolio_title, keywords)
            print(f"{filename} 파일의 키워드가 처리 및 저장 완료")

# DB에 저장(테스트 이후 진행)
@transaction.atomic
def save_to_database(portfolio_title, keywords):
    portfolio, created = PortfolioBoard.objects.get_or_create(board_title=portfolio_title)
    PortfolioKeyword.objects.filter(portfolio=portfolio).delete()
    for keyword, frequency in keywords:
        PortfolioKeyword.objects.create(
            portfolio=portfolio,
            portfolio_name=portfolio_title,
            keyword=keyword,
            frequency=frequency
        )

if __name__ == "__main__":
    # 스크립트 실행
    current_dir = os.path.dirname(os.path.abspath(__file__))
    pdf_folder = os.path.join(current_dir, "..", "pdf_files")
    stopwords_path = os.path.join(pdf_folder, "stopword.txt")
    stopwords = load_stopwords(stopwords_path)
    process_txt_files(pdf_folder, stopwords)