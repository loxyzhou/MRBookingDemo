from django.db import models

# Create your models here.
from django.contrib.auth.models import AbstractUser


class UserInfo(AbstractUser):
    """
    User Table
    """
    phone = models.CharField(max_length=32, default='80008000')
    sex_choice = (
        (1, 'M'),
        (2, 'F')
    )
    sex = models.IntegerField(choices=sex_choice,default=1)
    email = models.EmailField(max_length=32)


class MeetingRoom(models.Model):
    """
    Meeting Room Table
    """
    caption = models.CharField(max_length=32)
    num = models.IntegerField()

    def __str__(self):
        return self.caption


class RoomBooking(models.Model):
    """
    Room Booking Table
    """
    user = models.ForeignKey(to='UserInfo', on_delete=models.CASCADE)
    room = models.ForeignKey(to='MeetingRoom', on_delete=models.CASCADE)
    date = models.DateField()
    time_choices = (
        (1, '8:00'),
        (2, '9:00'),
        (3, '10:00'),
        (4, '11:00'),
        (5, '12:00'),
        (6, '13:00'),
        (7, '14:00'),
        (8, '15:00'),
        (9, '16:00'),
        (10, '17:00'),
        (11, '18:00'),
        (12, '19:00'),
        (13, '20:00'),
    )
    time_id = models.IntegerField(choices=time_choices)

    class Meta:
        """
        Combination
        """
        unique_together = (
            ('room','date','time_id'),
        )

    def __str__(self):
        return str(self.user)+"has booked the "+str(self.room)+" successfully"
