import os
from django.conf import settings
class CustomCertMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        # 서버 시작 시 인증서 정보 로드 시도
        try:
            cert_path = os.path.join(settings.BASE_DIR, 'harvy_be', 'certs', 'server.crt')
            with open(cert_path, 'r') as f:
                self.server_cert = f.read()
        except Exception as e:
            print(f"인증서 로드 오류 >> {e}")
            self.server_cert = None
    def __call__(self, request):
        response = self.get_response(request)
        response['X-Test-Header'] = 'Test-Value'
        # 응답 헤더에 인증서 정보 추가
        if self.server_cert:
            # 헤더 크기 제한으로 인증서 대신 식별 정보 추가
            response['X-Certificate-Identity'] = 'IntermediateCA-Signed'
        return response