from django.contrib import admin
from .models import (
    Survey,
    Question,
    Track,
    # QuestionTrack,
    Option,
    Partnerships,
    Result,
    ContactInformation
)

admin.site.register(Survey)
admin.site.register(Question)
admin.site.register(Track)
# admin.site.register(QuestionTrack)
admin.site.register(Option)
admin.site.register(Result)
admin.site.register(Partnerships)
admin.site.register(ContactInformation)
