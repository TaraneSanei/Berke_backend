from django.contrib import admin
from meditation.models import Track, Course, Tag
from user.models import User, OTP
# Register your models here.
admin.site.register(User)
admin.site.register(OTP)
admin.site.register(Track)
admin.site.register(Course)
admin.site.register(Tag)
