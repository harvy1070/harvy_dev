import PyPDF2
import os

def extract_text_from_pdf(pdf_path):
    with open(pdf_path, 'rb') as file:
        reader = PyPDF2.PdfReader(file)
        text = ""
        for page in reader.pages:
            text += page.extract_text() + "\n"
    return text

def process_pdf_folder(folder_path):
    for filename in os.listdir(folder_path):
        if filename.endswith('.pdf'):
            pdf_path = os.path.join(folder_path, filename)
            print(f"Processing {filename}...")
            text = extract_text_from_pdf(pdf_path)
            
            # 추출된 텍스트를 파일로 저장
            txt_filename = os.path.splitext(filename)[0] + '.txt'
            txt_path = os.path.join(folder_path, txt_filename)
            with open(txt_path, 'w', encoding='utf-8') as txt_file:
                txt_file.write(text)
            
            print(f"Extracted text saved to {txt_filename}")

pdf_folder = "pdf_files/"
process_pdf_folder(pdf_folder)