class CustomCertMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        # 서버 시작 시 인증서 정보 로드 시도
        try:
            with open('harvy_be/certs/server.crt', 'r') as f:
                self.server_cert = f.read()
        except:
            self.server_cert = None
            
    def __call__(self, request):
        response = self.get_response(request)
        
        # 응답 헤더에 인증서 정보 추가
        if self.server_cert:
            # 헤더 크기 제한으로 인증서 대신 식별 정보 추가
            response['X-Certificate-Identity'] = 'IntermediateCA-Signed'
            
        return response