from django.db import models
from datetime import datetime
from mysite import settings

# Create your models here.
class end_user(models.Model):
    email = models.EmailField(primary_key = True, unique = True)
    firstName = models.CharField(max_length = 30)
    lastName = models.CharField(max_length = 30)
    accessID = models.ForeignKey('access_lvl', on_delete = models.PROTECT)
    password = models.CharField(max_length = 50)
    faceImgDir = models.FilePathField(path = settings.USER_FACE_DIR, allow_files=False, allow_folders=True, blank = True)

class access_lvl(models.Model):
    accessID = models.AutoField(primary_key = True)
    accessName = models.CharField(max_length = 20)

class activity_log(models.Model):
    activityID = models.AutoField(primary_key = True)
    email = models.ForeignKey('end_user', on_delete = models.PROTECT, blank=True, null=True)
    firstSeen = models.DateTimeField(default = datetime.now)
    lastSeen = models.DateTimeField()
    faceCaptureDir = models.FilePathField(path = settings.FACE_CAPTURE_DIR, allow_files=False, allow_folders=True)
    clipDir = models.FilePathField(path = settings.CLIP_DIR, allow_files=False, allow_folders=True)

class notification(models.Model):
    notifID = models.AutoField(primary_key = True)
    notifType = models.CharField(max_length = 20)
    notifDetails = models.CharField(max_length = 300)
    notifImgDir = models.FilePathField(path = settings.NOTIF_IMG_DIR, allow_files=False, allow_folders=True)
    isApproved = models.BooleanField(default = False)

class notification_recipient(models.Model):
    recipientID = models.AutoField(primary_key = True)
    accessID = models.ForeignKey('access_lvl', on_delete = models.PROTECT)
    notifID = models.ForeignKey('notification', on_delete = models.PROTECT)

class audit_log(models.Model):
    auditID = models.AutoField(primary_key = True)
    email = models.ForeignKey('end_user', on_delete = models.PROTECT, blank=True, null=True)
    notifID = models.IntegerField(blank=True, null=True)
    timestamp = models.DateTimeField()
    userAction = models.CharField(max_length = 100)
