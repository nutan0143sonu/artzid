# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from django.contrib.auth.models import Group
from django.utils.safestring import mark_safe

from app.models import *

class MyUserAdmin(admin.ModelAdmin):
    icon = '<i class="material-icons">account_circle</i>'
    list_display = ['id', 'email','user_type','uuid',
                    'is_active', 'last_login','action']
    list_display_links = ('email',)
    list_per_page = 50
    readonly_fields = []
    ordering = ('id',)
    search_fields = ('id', 'email','user_type' )
    def action(self, obj):
        return mark_safe("<a class='button btn' style='color:white; padding:0 1rem;' href='/admin/app/myuser/{}/delete/'>Delete</a>".format(obj.id))

    def save_model(self, request, obj, form, change):
        '''docstring'''
        if "password" in form.changed_data:
            formPassword = form.cleaned_data.get('password')
            obj.set_password(obj.password)
        obj.save()
admin.site.register(MyUser,MyUserAdmin)

class ArtistAdmin(admin.ModelAdmin):
    icon = '<i class="material-icons">color_lens</i>'
    list_display = ['id', 'contact_email','organisation','job_type','action']
    list_display_links = ('contact_email',)
    list_per_page = 50
    readonly_fields = []
    ordering = ('id',)
    search_fields = ('id', 'contact_email','organisation','job_type' )

        
    def action(self, obj):
        return mark_safe("<a class='button btn' style='color:white; padding:0 1rem;' href='/admin/app/artist/{}/delete/'>Delete</a>".format(obj.id))

admin.site.register(Artist,ArtistAdmin)

class ProfessionalAdmin(admin.ModelAdmin):
    icon = '<i class="material-icons">work</i>'
    list_display = ['id','user', 'artistic_profession','action']
    list_display_links = ('user',)
    list_per_page = 50
    readonly_fields = []
    ordering = ('id',)
    search_fields = ('id','user', 'artistic_profession', )

    
    def action(self, obj):
        return mark_safe("<a class='button btn' style='color:white; padding:0 1rem;' href='/admin/app/professional/{}/delete/'>Delete</a>".format(obj.id))

admin.site.register(Professional,ProfessionalAdmin)

class InstitutionAdmin(admin.ModelAdmin):
    icon = '<i class="material-icons">account_balance</i>'
    list_display = ['id','user','location', 'institution_type','action']
    list_display_links = ('user',)
    list_per_page = 50
    readonly_fields = []
    ordering = ('id',)
    search_fields = ('id','user','location' 'institution_type', )
  
    def action(self, obj):
        return mark_safe("<a class='button btn' style='color:white; padding:0 1rem;' href='/admin/app/institution/{}/delete/'>Delete</a>".format(obj.id))

admin.site.register(Institution,InstitutionAdmin)

class InterestAdmin(admin.ModelAdmin):
    icon = '<i class="material-icons">check_circle</i>'
    list_display = ['id', 'name', 'action','delete']
    list_display_links = None
    list_per_page = 50
    readonly_fields = []
    ordering = ('id',)
    search_fields = ('id', 'name', )

    def action(self, obj):
        return mark_safe("<a class='button btn' style='color:white; padding:0 1rem;' href='/admin/app/interest/{}/change/'>View</a>".format(obj.id))
    
    def delete(self, obj):
        return mark_safe("<a class='button btn' style='color:white; padding:0 1rem;' href='/admin/app/interest/{}/delete/'>Delete</a>".format(obj.id))

admin.site.register(Interest,InterestAdmin)

class GoalAdmin(admin.ModelAdmin):
    icon = '<i class="material-icons">trending_up</i>'
    list_display = ['id', 'name', 'action','delete']
    list_display_links = None
    list_per_page = 50
    readonly_fields = []
    ordering = ('id',)
    search_fields = ('id', 'name', )

    def action(self, obj):
        return mark_safe("<a class='button btn' style='color:white; padding:0 1rem;' href='/admin/app/goal/{}/change/'>View</a>".format(obj.id))
   
    def delete(self, obj):
        return mark_safe("<a class='button btn' style='color:white; padding:0 1rem;' href='/admin/app/goal/{}/delete/'>Delete</a>".format(obj.id))

admin.site.register(Goal,GoalAdmin)


class ServiceAdmin(admin.ModelAdmin):
    icon = '<i class="material-icons">build</i>'
    list_display = ['id', 'name', 'action','delete']
    list_display_links = None
    list_per_page = 50
    readonly_fields = []
    ordering = ('id',)
    search_fields = ('id', 'name', )

    def action(self, obj):
        return mark_safe("<a class='button btn' style='color:white; padding:0 1rem;' href='/admin/app/service/{}/change/'>View</a>".format(obj.id))

    def delete(self, obj):
        return mark_safe("<a class='button btn' style='color:white; padding:0 1rem;' href='/admin/app/service/{}/delete/'>Delete</a>".format(obj.id))

admin.site.register(Service,ServiceAdmin)

class OfferAdmin(admin.ModelAdmin):
    icon = '<i class="material-icons">local_offer</i>'
    list_display = ['id','name', 'action','delete']
    list_display_links = None
    list_per_page = 50
    readonly_fields = []
    ordering = ('id','name')
    search_fields = ('id', )

    def action(self, obj):
        return mark_safe("<a class='button btn' style='color:white; padding:0 1rem;' href='/admin/app/offer/{}/change/'>View</a>".format(obj.id))

    def delete(self, obj):
        return mark_safe("<a class='button btn' style='color:white; padding:0 1rem;' href='/admin/app/offer/{}/delete/'>Delete</a>".format(obj.id))

admin.site.register(Offer,OfferAdmin)


# class ArtistInterestAdmin(admin.ModelAdmin):
#     icon = '<i class="material-icons">accessibility</i>'
#     list_display = ['id','artist','interest','action']
#     list_display_links = ('artist',)
#     list_per_page = 50
#     readonly_fields = []
#     ordering = ('id',)
#     search_fields = ('id', )
  
#     def action(self, obj):
#         return mark_safe("<a class='button btn' style='color:white; padding:0 1rem;' href='/admin/app/artistinterest/{}/delete/'>Delete</a>".format(obj.id))

# admin.site.register(ArtistInterest,ArtistInterestAdmin)

# class ArtistGoalAdmin(admin.ModelAdmin):
#     icon = '<i class="material-icons">settings_input_svideo</i>'
#     list_display = ['id','artist', 'goal','action']
#     list_display_links = ('artist',)
#     list_per_page = 50
#     readonly_fields = []
#     ordering = ('id',)
#     search_fields = ('id', )

#     def action(self, obj):
#         return mark_safe("<a class='button btn' style='color:white; padding:0 1rem;' href='/admin/app/artistgoal/{}/delete/'>Delete</a>".format(obj.id))

# admin.site.register(ArtistGoal,ArtistGoalAdmin)



# class ProfessionalServicesAdmin(admin.ModelAdmin):
#     icon = '<i class="material-icons">account_balance</i>'
#     list_display = ['id','professional','service','action']
#     list_display_links = ('professional',)
#     list_per_page = 50
#     readonly_fields = []
#     ordering = ('id',)
#     search_fields = ('id', )

   
#     def action(self, obj):
#         return mark_safe("<a class='button btn' style='color:white; padding:0 1rem;' href='/admin/app/professionalservices/{}/delete/'>Delete</a>".format(obj.id))

# admin.site.register(ProfessionalServices,ProfessionalServicesAdmin)


# class ProfessionalGoalAdmin(admin.ModelAdmin):
#     icon = '<i class="material-icons">business</i>'
#     list_display = ['id','professional','goal','action']
#     list_display_links = ('professional',)
#     list_per_page = 50
#     readonly_fields = []
#     ordering = ('id',)
#     search_fields = ('id',)

   
#     def action(self, obj):
#         return mark_safe("<a class='button btn' style='color:white; padding:0 1rem;' href='/admin/app/professionalgoal/{}/delete/'>Delete</a>".format(obj.id))

# admin.site.register(ProfessionalGoal,ProfessionalGoalAdmin)



# class InstitutionOfferAdmin(admin.ModelAdmin):
#     icon = '<i class="material-icons">account_balance</i>'
#     list_display = ['id','institution','offer','action']
#     list_display_links = ('institution',)
#     list_per_page = 50
#     readonly_fields = []
#     ordering = ('id',)
#     search_fields = ('id','institution','offer')

   
#     def action(self, obj):
#         return mark_safe("<a class='button btn' style='color:white; padding:0 1rem;' href='/admin/app/institutionoffer/{}/delete/'>Delete</a>".format(obj.id))

# admin.site.register(InstitutionOffer,InstitutionOfferAdmin)


class SocialAdmin(admin.ModelAdmin):
    icon = '<i class="material-icons">contact_mail</i>'
    list_display = ['id','user','website','instagram','facebook','action']
    list_display_links = ('user',)
    list_per_page = 50
    readonly_fields = []
    ordering = ('id','website','instagram','facebook')
    search_fields = ('id', )

    
    def action(self, obj):
        return mark_safe("<a class='button btn' style='color:white; padding:0 1rem;' href='/admin/app/social/{}/delete/'>Delete</a>".format(obj.id))

admin.site.register(Social,SocialAdmin)

class BlogAdmin(admin.ModelAdmin):
    icon = '<i class="material-icons">book</i>'
    list_display = ['id','user','title','created_at','action']
    list_display_links = ('user',)
    list_per_page = 50
    readonly_fields = []
    ordering = ('id','user','title','created_at')
    search_fields = ('id', 'title','user')

    def action(self, obj):
        return mark_safe("<a class='button btn' style='color:white; padding:0 1rem;' href='/admin/app/blog/{}/delete/'>Delete</a>".format(obj.id))

admin.site.register(Blog,BlogAdmin)


class CommentAdmin(admin.ModelAdmin):
    icon = '<i class="material-icons">comment</i>'
    list_display = ['id','user','blog','created_at','action']
    list_display_links = ('user',)
    list_per_page = 50
    readonly_fields = []
    ordering = ('id','user','blog','created_at')
    search_fields = ('id', 'blog','user')

    
    def action(self, obj):
        return mark_safe("<a class='button btn' style='color:white; padding:0 1rem;' href='/admin/app/comment/{}/delete/'>Delete</a>".format(obj.id))

admin.site.register(Comment,CommentAdmin)


class FollowAdmin(admin.ModelAdmin):
    icon = '<i class="material-icons">person_add</i>'
    list_display = ['id','user','to_follower','is_follow','action']
    list_display_links = ('user',)
    list_per_page = 50
    readonly_fields = []
    ordering = ('id','user','to_follower','created_at')
    search_fields = ('id', 'to_follower','user')

    
    def action(self, obj):
        return mark_safe("<a class='button btn' style='color:white; padding:0 1rem;' href='/admin/app/follow/{}/delete/'>Delete</a>".format(obj.id))

admin.site.register(Follow,FollowAdmin)


class ConnectAdmin(admin.ModelAdmin):
    icon = '<i class="material-icons">add</i>'
    list_display = ['id','user','connect','is_connect','action']
    list_display_links = ('user',)
    list_per_page = 50
    readonly_fields = []
    ordering = ('id','user','connect','created_at')
    search_fields = ('id', 'connect','user')

    
    def action(self, obj):
        return mark_safe("<a class='button btn' style='color:white; padding:0 1rem;' href='/admin/app/connect/{}/delete/'>Delete</a>".format(obj.id))

admin.site.register(Connect,ConnectAdmin)


class PhotosAdmin(admin.ModelAdmin):
    icon = '<i class="material-icons">camera</i>'
    list_display = ['id','user','title','created_at','action']
    list_display_links = ('user',)
    list_per_page = 50
    readonly_fields = []
    ordering = ('id','user','title','created_at')
    search_fields = ('id', 'title','user')

    
    def action(self, obj):
        return mark_safe("<a class='button btn' style='color:white; padding:0 1rem;' href='/admin/app/photos/{}/delete/'>Delete</a>".format(obj.id))

admin.site.register(Photos,PhotosAdmin)


class GalleryAdmin(admin.ModelAdmin):
    icon = '<i class="material-icons"> photo </i>'
    list_display = ['id','user','title','created_at','action']
    list_display_links = ('user',)
    list_per_page = 50
    readonly_fields = []
    ordering = ('id','user','title','created_at')
    search_fields = ('id', 'title','user')

    def action(self, obj):
        return mark_safe("<a class='button btn' style='color:white; padding:0 1rem;' href='/admin/app/gallery/{}/delete/'>Delete</a>".format(obj.id))

admin.site.register(Gallery,GalleryAdmin)

class ProjectAdmin(admin.ModelAdmin):
    icon = '<i class="material-icons">folder</i>'
    list_display = ['id','user','title','created_at','action']
    list_display_links = ('user',)
    list_per_page = 50
    readonly_fields = []
    ordering = ('id','user','title','created_at')
    search_fields = ('id', 'title','user')

    def action(self, obj):
        return mark_safe("<a class='button btn' style='color:white; padding:0 1rem;' href='/admin/app/project/{}/delete/'>Delete</a>".format(obj.id))

admin.site.register(Project,ProjectAdmin)

class BioAdmin(admin.ModelAdmin):
    icon = '<i class="material-icons">face</i>'
    list_display = ['id','user','action']
    list_display_links = ('user',)
    list_per_page = 50
    readonly_fields = []
    ordering = ('id','user',)
    search_fields = ('id','user')

    def action(self, obj):
        return mark_safe("<a class='button btn' style='color:white; padding:0 1rem;' href='/admin/app/bio/{}/delete/'>Delete</a>".format(obj.id))

admin.site.register(Bio,BioAdmin)

class BioEducationAdmin(admin.ModelAdmin):
    icon = '<i class="material-icons">face</i>'
    list_display = ['id','user','action']
    list_display_links = ('user',)
    list_per_page = 50
    readonly_fields = []
    ordering = ('id','user',)
    search_fields = ('id','user')

    def action(self, obj):
        return mark_safe("<a class='button btn' style='color:white; padding:0 1rem;' href='/admin/app/bioeducation/{}/delete/'>Delete</a>".format(obj.id))

admin.site.register(BioEducation,BioEducationAdmin)

class BiographyLinkAdmin(admin.ModelAdmin):
    icon = '<i class="material-icons">face</i>'
    list_display = ['id','user','action']
    list_display_links = ('user',)
    list_per_page = 50
    readonly_fields = []
    ordering = ('id','user',)
    search_fields = ('id','user')

    def action(self, obj):
        return mark_safe("<a class='button btn' style='color:white; padding:0 1rem;' href='/admin/app/biographylink/{}/delete/'>Delete</a>".format(obj.id))

admin.site.register(BiographyLink,BiographyLinkAdmin)

class RatingAdmin(admin.ModelAdmin):
    icon = '<i class="material-icons">stars</i>'
    list_display = ['id','user','action']
    list_display_links = ('user',)
    list_per_page = 50
    readonly_fields = []
    ordering = ('id','user',)
    search_fields = ('id','user')

    def action(self, obj):
        return mark_safe("<a class='button btn' style='color:white; padding:0 1rem;' href='/admin/app/rating/{}/delete/'>Delete</a>".format(obj.id))

admin.site.register(Rating,RatingAdmin)

class UserSkillAdmin(admin.ModelAdmin):
    icon = '<i class="material-icons">casino</i>'
    list_display = ['id','name','action']
    list_display_links = ('name',)
    list_per_page = 50
    readonly_fields = []
    ordering = ('id','name',)
    search_fields = ('id','name')

    def action(self, obj):
        return mark_safe("<a class='button btn' style='color:white; padding:0 1rem;' href='/admin/app/userskill/{}/delete/'>Delete</a>".format(obj.id))

admin.site.register(UserSkill,UserSkillAdmin)


class ArtistUserSkillAdmin(admin.ModelAdmin):
    icon = '<i class="material-icons">streetview</i>'
    list_display = ['id','user','action']
    list_display_links = ('user',)
    list_per_page = 50
    readonly_fields = []
    ordering = ('id','user',)
    search_fields = ('id','user')

    def action(self, obj):
        return mark_safe("<a class='button btn' style='color:white; padding:0 1rem;' href='/admin/app/artistuserskill/{}/delete/'>Delete</a>".format(obj.id))

admin.site.register(ArtistUserSkill,ArtistUserSkillAdmin)

class UserInterestAdmin(admin.ModelAdmin):
    icon = '<i class="material-icons">casino</i>'
    list_display = ['id','name','action']
    list_display_links = ('name',)
    list_per_page = 50
    readonly_fields = []
    ordering = ('id','name',)
    search_fields = ('id','name')

    def action(self, obj):
        return mark_safe("<a class='button btn' style='color:white; padding:0 1rem;' href='/admin/app/userinterest/{}/delete/'>Delete</a>".format(obj.id))

admin.site.register(UserInterest,UserInterestAdmin)

class ArtistUserInterestAdmin(admin.ModelAdmin):
    icon = '<i class="material-icons">golf_course</i>'
    list_display = ['id','user','action']
    list_display_links = ('user',)
    list_per_page = 50
    readonly_fields = []
    ordering = ('id','user',)
    search_fields = ('id','user')

    def action(self, obj):
        return mark_safe("<a class='button btn' style='color:white; padding:0 1rem;' href='/admin/app/artistuserinterest/{}/delete/'>Delete</a>".format(obj.id))

admin.site.register(ArtistUserInterest,ArtistUserInterestAdmin)

class ArtistAchievementAdmin(admin.ModelAdmin):
    icon = '<i class="material-icons">account_circle</i>'
    list_display = ['id','user','achievement','no','action']
    list_display_links = ('user',)
    list_per_page = 50
    readonly_fields = []
    ordering = ('id','user',)
    search_fields = ('id','user')

    def action(self, obj):
        return mark_safe("<a class='button btn' style='color:white; padding:0 1rem;' href='/admin/app/artistachievement/{}/delete/'>Delete</a>".format(obj.id))

admin.site.register(ArtistAchievement,ArtistAchievementAdmin)


class ArtistExhibitionsAdmin(admin.ModelAdmin):
    icon = '<i class="material-icons">account_circle</i>'
    list_display = ['id','user','exhibitions','no','action']
    list_display_links = ('user',)
    list_per_page = 50
    readonly_fields = []
    ordering = ('id','user',)
    search_fields = ('id','user')

    def action(self, obj):
        return mark_safe("<a class='button btn' style='color:white; padding:0 1rem;' href='/admin/app/artistexhibitions/{}/delete/'>Delete</a>".format(obj.id))

admin.site.register(ArtistExhibitions,ArtistExhibitionsAdmin)

class UserServiceAdmin(admin.ModelAdmin):
    icon = '<i class="material-icons">build</i>'
    list_display = ['id','name','action']
    list_display_links = ('name',)
    list_per_page = 50
    readonly_fields = []
    ordering = ('id','name',)
    search_fields = ('id','name')

    def action(self, obj):
        return mark_safe("<a class='button btn' style='color:white; padding:0 1rem;' href='/admin/app/userservice/{}/delete/'>Delete</a>".format(obj.id))

admin.site.register(UserService,UserServiceAdmin)

class AddUserServiceAdmin(admin.ModelAdmin):
    icon = '<i class="material-icons">work</i>'
    list_display = ['id','user','service','action']
    list_display_links = ('user',)
    list_per_page = 50
    readonly_fields = []
    ordering = ('id','user',)
    search_fields = ('id','user')

    def action(self, obj):
        return mark_safe("<a class='button btn' style='color:white; padding:0 1rem;' href='/admin/app/adduserservice/{}/delete/'>Delete</a>".format(obj.id))

admin.site.register(AddUserService,AddUserServiceAdmin)

class AddClientAdmin(admin.ModelAdmin):
    icon = '<i class="material-icons">supervisor_account</i>'
    list_display = ['id','user','action']
    list_display_links = ('user',)
    list_per_page = 50
    readonly_fields = []
    ordering = ('id','user',)
    search_fields = ('id','user')

    def action(self, obj):
        return mark_safe("<a class='button btn' style='color:white; padding:0 1rem;' href='/admin/app/addclient/{}/delete/'>Delete</a>".format(obj.id))

admin.site.register(AddClient,AddClientAdmin)

class BrandAdmin(admin.ModelAdmin):
    icon = '<i class="material-icons">healing</i>'
    list_display = ['id','name','action']
    list_display_links = ('name',)
    list_per_page = 50
    readonly_fields = []
    ordering = ('id','name',)
    search_fields = ('id','name')

    def action(self, obj):
        return mark_safe("<a class='button btn' style='color:white; padding:0 1rem;' href='/admin/app/brand/{}/delete/'>Delete</a>".format(obj.id))

admin.site.register(Brand,BrandAdmin)

class AddBrandAdmin(admin.ModelAdmin):
    icon = '<i class="material-icons">healing</i>'
    list_display = ['id','user','action']
    list_display_links = ('user',)
    list_per_page = 50
    readonly_fields = []
    ordering = ('id','user',)
    search_fields = ('id','user')

    def action(self, obj):
        return mark_safe("<a class='button btn' style='color:white; padding:0 1rem;' href='/admin/app/addbrand/{}/delete/'>Delete</a>".format(obj.id))

admin.site.register(AddBrand,AddBrandAdmin)

class AddTeamAdmin(admin.ModelAdmin):
    icon = '<i class="material-icons">group_add</i>'
    list_display = ['id','user','action']
    list_display_links = ('user',)
    list_per_page = 50
    readonly_fields = []
    ordering = ('id','user',)
    search_fields = ('id','user')

    def action(self, obj):
        return mark_safe("<a class='button btn' style='color:white; padding:0 1rem;' href='/admin/app/addteam/{}/delete/'>Delete</a>".format(obj.id))

admin.site.register(AddTeam,AddTeamAdmin)

class ActivityAdmin(admin.ModelAdmin):
    icon = '<i class="material-icons">directions_run</i>'
    list_display = ['id','name','action']
    list_display_links = ('name',)
    list_per_page = 50
    readonly_fields = []
    ordering = ('id','name',)
    search_fields = ('id','name')

    def action(self, obj):
        return mark_safe("<a class='button btn' style='color:white; padding:0 1rem;' href='/admin/app/activity/{}/delete/'>Delete</a>".format(obj.id))

admin.site.register(Activity,ActivityAdmin)

class InstitutionInformationAdmin(admin.ModelAdmin):
    icon = '<i class="material-icons">location_city</i>'
    list_display = ['id','user','action']
    list_display_links = ('user',)
    list_per_page = 50
    readonly_fields = []
    ordering = ('id','user',)
    search_fields = ('id','user')

    def action(self, obj):
        return mark_safe("<a class='button btn' style='color:white; padding:0 1rem;' href='/admin/app/institutioninformation/{}/delete/'>Delete</a>".format(obj.id))

admin.site.register(InstitutionInformation,InstitutionInformationAdmin)

class MediaAdmin(admin.ModelAdmin):
    icon = '<i class="material-icons">add_a_photo</i>'
    list_display = ['id','image','action']
    list_display_links = ('image',)
    list_per_page = 50
    readonly_fields = []
    ordering = ('id','image',)
    search_fields = ('id','image')

    def action(self, obj):
        return mark_safe("<a class='button btn' style='color:white; padding:0 1rem;' href='/admin/app/media/{}/delete/'>Delete</a>".format(obj.id))

admin.site.register(Media,MediaAdmin)

class VideoAndImageAdmin(admin.ModelAdmin):
    icon = '<i class="material-icons">add_a_photo</i>'
    list_display = ['id','image','action']
    list_display_links = ('image',)
    list_per_page = 50
    readonly_fields = []
    ordering = ('id','image',)
    search_fields = ('id','image')

    def action(self, obj):
        return mark_safe("<a class='button btn' style='color:white; padding:0 1rem;' href='/admin/app/videoandimage/{}/delete/'>Delete</a>".format(obj.id))

admin.site.register(VideoAndImage,VideoAndImageAdmin)

class AddMediaInProjectAdmin(admin.ModelAdmin):
    icon = '<i class="material-icons">add_a_photo</i>'
    list_display = ['id','image','action']
    list_display_links = ('image',)
    list_per_page = 50
    readonly_fields = []
    ordering = ('id','image',)
    search_fields = ('id','image')

    def action(self, obj):
        return mark_safe("<a class='button btn' style='color:white; padding:0 1rem;' href='/admin/app/addmediainproject/{}/delete/'>Delete</a>".format(obj.id))

admin.site.register(AddMediaInProject,AddMediaInProjectAdmin)

class AddMediaInWorkAdmin(admin.ModelAdmin):
    icon = '<i class="material-icons">add_a_photo</i>'
    list_display = ['id','image','action']
    list_display_links = ('image',)
    list_per_page = 50
    readonly_fields = []
    ordering = ('id','image',)
    search_fields = ('id','image')

    def action(self, obj):
        return mark_safe("<a class='button btn' style='color:white; padding:0 1rem;' href='/admin/app/addmediainwork/{}/delete/'>Delete</a>".format(obj.id))

admin.site.register(AddMediaInWork,AddMediaInWorkAdmin)

class MediaDetailsAdmin(admin.ModelAdmin):
    icon = '<i class="material-icons">collections</i>'
    list_display = ['id','user','thumbnail','action']
    list_display_links = ('user',)
    list_per_page = 50
    readonly_fields = []
    ordering = ('id','user',)
    search_fields = ('id','user')

    def action(self, obj):
        return mark_safe("<a class='button btn' style='color:white; padding:0 1rem;' href='/admin/app/mediadetails/{}/delete/'>Delete</a>".format(obj.id))

admin.site.register(MediaDetails,MediaDetailsAdmin)

class ArtistAddAdmin(admin.ModelAdmin):
    icon = '<i class="material-icons">supervisor_account</i>'
    list_display = ['id','user','artist','action']
    list_display_links = ('user',)
    list_per_page = 50
    readonly_fields = []
    ordering = ('id','user',)
    search_fields = ('id','user')

    def action(self, obj):
        return mark_safe("<a class='button btn' style='color:white; padding:0 1rem;' href='/admin/app/artistadd/{}/delete/'>Delete</a>".format(obj.id))

admin.site.register(ArtistAdd,ArtistAddAdmin)


class PlaceAdmin(admin.ModelAdmin):
    icon = '<i class="material-icons">my_location</i>'
    list_display = ['id','user','place','action']
    list_display_links = ('user',)
    list_per_page = 50
    readonly_fields = []
    ordering = ('id','user',)
    search_fields = ('id','user')

    def action(self, obj):
        return mark_safe("<a class='button btn' style='color:white; padding:0 1rem;' href='/admin/app/place/{}/delete/'>Delete</a>".format(obj.id))

admin.site.register(Place,PlaceAdmin)

class ArtistSalesAdmin(admin.ModelAdmin):
    icon = '<i class="material-icons">library_add</i>'
    list_display = ['id','user','sales','action']
    list_display_links = ('user',)
    list_per_page = 50
    readonly_fields = []
    ordering = ('id','user',)
    search_fields = ('id','user')

    def action(self, obj):
        return mark_safe("<a class='button btn' style='color:white; padding:0 1rem;' href='/admin/app/artistsales/{}/delete/'>Delete</a>".format(obj.id))

admin.site.register(ArtistSales,ArtistSalesAdmin)

class UserProjectAdmin(admin.ModelAdmin):
    icon = '<i class="material-icons">create_new_folder</i>'
    list_display = ['id','user','project','no','action']
    list_display_links = ('user',)
    list_per_page = 50
    readonly_fields = []
    ordering = ('id','user',)
    search_fields = ('id','user')

    def action(self, obj):
        return mark_safe("<a class='button btn' style='color:white; padding:0 1rem;' href='/admin/app/userproject/{}/delete/'>Delete</a>".format(obj.id))

admin.site.register(UserProject,UserProjectAdmin)


class InstitutionActivityAdmin(admin.ModelAdmin):
    icon = '<i class="material-icons">stars</i>'
    list_display = ['id','user','activity','action']
    list_display_links = ('user',)
    list_per_page = 50
    readonly_fields = []
    ordering = ('id','user',)
    search_fields = ('id','user')

    def action(self, obj):
        return mark_safe("<a class='button btn' style='color:white; padding:0 1rem;' href='/admin/app/institutionactivity/{}/delete/'>Delete</a>".format(obj.id))

admin.site.register(InstitutionActivity,InstitutionActivityAdmin)

admin.site.unregister(Group)

