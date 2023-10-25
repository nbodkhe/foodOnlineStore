from django.db import models

import vendor
from accounts.models import User, UserProfile
from accounts.utils import send_notification


# Create your models here.
class Vendor(models.Model):
    user = models.OneToOneField(User, related_name='user', on_delete=models.CASCADE)
    user_profile = models.OneToOneField(UserProfile, related_name='userprofile', on_delete=models.CASCADE)
    vendor_name = models.CharField(max_length=50)
    vendor_slug = models.SlugField(max_length=100, unique=True)
    vendor_license = models.ImageField(upload_to='vendor/license')
    is_approved = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.vendor_name

    # def save(self, *args, **kwargs):
    #     if self.pk is not None:
    #         #update
    #         orig = Vendor.objects.get(pk=self.pk)
    #         if orig.is_approved != self.is_approved:
    #             mail_subject = 'Congregations ! your restaurant has been approved.'
    #             mail_template = 'accounts/emails/approval_email.html'
    #             context = {
    #                 'user': self.user,
    #                 'is_approved': self.is_approved,
    #             }
    #             if self.is_approved == True:
    #                 # Send notification mail
    #
    #                 send_notification(mail_subject, mail_template, context)
    #             else:
    #                 mail_subject = 'We are sorry You are not eligible for publishing your food menu on our restaurant'
    #                 send_notification(mail_subject, mail_template, context)
    #
    #     return super(Vendor, self).save(*args, **kwargs)

    def save(self, *args, **kwargs):
        if self.pk is not None:
            # Update
            orig = Vendor.objects.get(pk=self.pk)
            if orig.is_approved != self.is_approved:
                mail_subject = 'Congratulations! Your restaurant has been approved.'
                mail_template = 'accounts/emails/approval_email.html'
                context = {
                    'user': self.user,
                    'is_approved': self.is_approved,
                }
                if self.is_approved == True:
                    # Send notification mail
                    send_notification(mail_subject, mail_template, context)
                else:
                    mail_subject = 'We are sorry, you are not eligible for publishing your food menu on our restaurant'
                    send_notification(mail_subject, mail_template, context)

        return super(Vendor, self).save(*args, **kwargs)
