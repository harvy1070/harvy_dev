from django.contrib import admin

from .models import UserInfo, QnA, PortfolioBoard, PortfolioFiles, PjTimeline

admin.site.register(UserInfo)
admin.site.register(QnA)
admin.site.register(PortfolioBoard)
admin.site.register(PortfolioFiles)
admin.site.register(PjTimeline)