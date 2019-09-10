from __future__ import unicode_literals

from django.contrib import admin
from django.contrib.auth.models import Group
from django.utils.safestring import mark_safe

from static_content.models import *

class PrivacyPolicyAdmin(admin.ModelAdmin):
    icon = '<i class="material-icons">lock</i>'
    list_display = ['id','title','action']
    list_display_links = ('title',)
    list_per_page = 50
    readonly_fields = []
    ordering = ('id',)
    search_fields = ('id', 'title',)

        
    def action(self, obj):
        return mark_safe("<a class='button btn' style='color:white; padding:0 1rem;' href='/admin/app/privacypolicy/{}/delete/'>Delete</a>".format(obj.id))

admin.site.register(PrivacyPolicy,PrivacyPolicyAdmin)

class AboutUsAdmin(admin.ModelAdmin):
    icon = '<i class="material-icons">people</i>'
    list_display = ['id','title','action']
    list_display_links = ('title',)
    list_per_page = 50
    readonly_fields = []
    ordering = ('id',)
    search_fields = ('id', 'title',)

        
    def action(self, obj):
        return mark_safe("<a class='button btn' style='color:white; padding:0 1rem;' href='/admin/app/aboutus/{}/delete/'>Delete</a>".format(obj.id))

admin.site.register(AboutUs,AboutUsAdmin)

class TermsAndConditionsAdmin(admin.ModelAdmin):
    icon = '<i class="material-icons">description</i>'
    list_display = ['id','title','action']
    list_display_links = ('title',)
    list_per_page = 50
    readonly_fields = []
    ordering = ('id',)
    search_fields = ('id', 'title',)

        
    def action(self, obj):
        return mark_safe("<a class='button btn' style='color:white; padding:0 1rem;' href='/admin/app/termsandconditions/{}/delete/'>Delete</a>".format(obj.id))

admin.site.register(TermsAndConditions,TermsAndConditionsAdmin)

class CareersAdmin(admin.ModelAdmin):
    icon = '<i class="material-icons">work</i>'
    list_display = ['id','email','action']
    list_display_links = ('email',)
    list_per_page = 50
    readonly_fields = []
    ordering = ('id',)
    search_fields = ('id', 'email',)

        
    def action(self, obj):
        return mark_safe("<a class='button btn' style='color:white; padding:0 1rem;' href='/admin/app/career/{}/delete/'>Delete</a>".format(obj.id))

admin.site.register(Careers,CareersAdmin)