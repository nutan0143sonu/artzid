from django.db import models
from cloudinary.models import CloudinaryField
from djrichtextfield.models import RichTextField


class PrivacyPolicy(models.Model):
    title = models.CharField("Title", max_length=255, blank=True, null=True)
    description = RichTextField("Description", blank=True, null=True)

    def __str__(self):
        return "Privacy Policy"

    class Meta:
        verbose_name_plural = "Privacy Policy"


class TermsAndConditions(models.Model):
    title = models.CharField("Title", max_length=255, blank=True, null=True)
    description = RichTextField("Description", blank=True, null=True)

    def __str__(self):
        return "Terms and conditions"

    class Meta:
        verbose_name_plural = "Terms And Condition"


class AboutUs(models.Model):
    title = models.CharField("Title", max_length=255, blank=True, null=True)
    description = RichTextField("Description", blank=True, null=True)

    def __str__(self):
        return "AboutUs"

    class Meta:
        verbose_name_plural = "About Us"

class Careers(models.Model):
    first_name = models.CharField("First Name", max_length=255)
    last_name = models.CharField("Last Name", max_length=255)
    email = models.EmailField("email", max_length=255)
    file = CloudinaryField(null=True,blank=True)
    message = models.TextField("message",max_length=500)

    class Meta:
        verbose_name_plural = "Careers"