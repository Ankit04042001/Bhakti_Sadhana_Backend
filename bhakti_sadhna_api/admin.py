from django.contrib import admin
from .models import User, Otp, Attendence, Task
from django.contrib.auth.models import Group
from .forms import UserAdmin

admin.site.register(User, UserAdmin)
admin.site.unregister(Group)
admin.site.register(Otp)
admin.site.register(Attendence)
admin.site.register(Task)




