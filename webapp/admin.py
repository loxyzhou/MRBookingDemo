from django.contrib import admin
from webapp.models import RoomBooking,MeetingRoom,UserInfo
admin.site.register(UserInfo)
admin.site.register(MeetingRoom)
admin.site.register(RoomBooking)