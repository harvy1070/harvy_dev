from django.contrib import admin

from .models import *

admin.site.register(UserInfo)
admin.site.register(QnA)
admin.site.register(PortfolioBoard)
admin.site.register(PortfolioFiles)
admin.site.register(PjTimeline)
admin.site.register(ChatSession)
admin.site.register(ChatMessage)
admin.site.register(UserPreference)
admin.site.register(PortfolioKeyword)