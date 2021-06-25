from django.contrib import admin
from .models import FalseInformation, RFRModel, FeedbackModel

# Register your models here.
admin.register(FalseInformation)
admin.register(RFRModel)
admin.register(FeedbackModel)