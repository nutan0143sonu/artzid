from rest_framework import serializers
from rest_framework.serializers import SerializerMethodField

from django.utils.functional import lazy, SimpleLazyObject

from cloudinary.uploader import upload


from .models import *
from app.models import *


class ArtistSignupSerializers(serializers.ModelSerializer):
    def create(self, validated_data):
        params = self.context.get('params')
        user = MyUser.objects.create(**validated_data)
        user.set_password(params['password'])
        user.otp_creation()
        user.save()

        artist_user = Artist.objects.create(user=user, **params['artist'])
        if 'interest' in params:
            for data in params['interest']:
                try:
                    interest = Interest.objects.get(id=data)
                    ArtistInterest.objects.create(artist=artist_user, interest=interest)
                  
                except Exception as e:
                    print("ARTIST INTREST Exception", e)
        if 'goal' in params:
            for data in params['goal']:
                try:
                    goal = Goal.objects.get(id=data)
                    ArtistGoal.objects.create(artist=artist_user, goal=goal)
                    
                except Exception as e:
                    print("ARTIST Goal Exception", e)
        Social.objects.create(user=user, **params['social'])
        return user

    class Meta:
        model = MyUser
        fields = "__all__"

class InstitutionSignupSerializers(serializers.ModelSerializer):
    def create(self, validated_data):
        params = self.context.get('params')
        user = MyUser.objects.create(**validated_data)
        user.set_password(params['password'])
        user.otp_creation()
        user.save()

        institution_user = Institution.objects.create(user=user, **params['institution'])
        if 'offer' in params:
            for data in params['offer']:
                try:
                    offer = Offer.objects.get(id=data)
                    InstitutionOffer.objects.create(institution=institution_user, offer=offer)
                except Exception as e:
                    print("institution_user Offer Exception", e)
        Social.objects.create(user=user, **params['social'])
        return user

    class Meta:
        model = MyUser
        fields = "__all__"

class ProfessionalSignupSerializers(serializers.ModelSerializer):
    def create(self, validated_data):
        params = self.context.get('params')
        user = MyUser.objects.create(**validated_data)
        user.set_password(params['password'])
        user.otp_creation()
        user.save()
        if 'professional' in params:
            professional_params = params['professional']
            if 'job_type' in professional_params:
                if professional_params['job_type'] == "Self employee":
                    professional_user = Professional.objects.create(user=user,
                                                                    artistic_profession=professional_params[
                                                                        'artistic_profession']
                                                                    , job_type=professional_params['job_type'])
                else:
                    professional_user = Professional.objects.create(user=user,
                                                                    artistic_profession=professional_params[
                                                                        'artistic_profession'],
                                                                    job_type='Work for',
                                                                    organisation=professional_params['organisation'])
        if 'service' in params:
            for data in params['service']:
                try:
                    service = Service.objects.get(id=data)
                    ProfessionalServices.objects.create(professional=professional_user,
                                                                              service=service)
                    obj.save()
                except Exception as e:
                    print("institution_user Offer Exception", e)
        if 'goal' in params:
            for data in params['goal']:
                try:
                    goal = Goal.objects.get(id=data)
                    ProfessionalGoal.objects.create(professional=professional_user, goal=goal)
                except Exception as e:
                    print("ARTIST Goal Exception", e)
        Social.objects.create(user=user, **params['social'])
        return user

    class Meta:
        model = MyUser
        fields = "__all__"


class LoginSerializer(serializers.ModelSerializer):
    image = SerializerMethodField()
   
    def get_image(self,obj):
        if obj.image:
            return obj.image.url
        return 'null'
         
    class Meta:
        model = MyUser
        exclude = ('password', 'last_login', 'updated_at', 'otp',
                   'is_superuser', 'is_staff', 'created_at',
                   'groups', 'user_permissions', 'deleted_at')

class BlogSerializer(serializers.ModelSerializer):
    class Meta:
        model = Blog
        fields = "__all__"

class SocialInstituionalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Social
        fields = "__all__"

#----------------------------------------Get-All-Artist-User-Serializer-----------------------------------------------
class ArtistIntrestSerializer(serializers.ModelSerializer):
    interest=SerializerMethodField()
    def get_interest(self,obj):
        if obj.interest:
            return obj.interest.name
    class Meta:
        model = ArtistInterest
        fields = ('id','interest',)

class ArtistGoalSerializer(serializers.ModelSerializer):
    goal=SerializerMethodField()
    def get_goal(self,obj):
        if obj.goal:
            return obj.goal.name
    class Meta:
        model = ArtistGoal
        fields = ('id','goal',)

class GetAllArtistUserSerializer(serializers.ModelSerializer):
    artist_interest=ArtistIntrestSerializer(many=True)
    artist_goal=ArtistGoalSerializer(many=True)
            
    class Meta:
        model = Artist
        fields = "__all__"

class ArtistUserserializer(serializers.ModelSerializer):
    social_user = SocialInstituionalSerializer(many=True)
    artist_user = GetAllArtistUserSerializer(many=True)
    class Meta:
        model = MyUser
        fields = ('uuid','email','user_type','social_user','artist_user',)

#----------------------------------------Get-All-Professional-User-Serializer----------------------------------------------

class ProfessionalServicesSerializer(serializers.ModelSerializer):
    service=SerializerMethodField()

    def get_service(self,obj):
        if obj.service:
            return obj.service.name

    class Meta:
            model = ProfessionalServices
            fields =("id","service",)

class ProfessionalGoalSerializer(serializers.ModelSerializer):

    goal=SerializerMethodField()
    def get_goal(self,obj):
        if obj.goal:
            return obj.goal.name

    class Meta:
            model = ProfessionalGoal
            fields = ("id","goal",)

class GetAllProfessionalUserSerializer(serializers.ModelSerializer):
    professional_service=ProfessionalServicesSerializer(many=True)
    professional_goal=ProfessionalGoalSerializer(many=True)
    class Meta:
        model = Professional
        fields ="__all__"

class ProfessionalUserserializer(serializers.ModelSerializer):
    social_user = SocialInstituionalSerializer(many=True)
    professional_user = GetAllProfessionalUserSerializer(many=True)
    class Meta:
        model = MyUser
        fields = ('uuid','email','user_type','social_user','professional_user',)

#--------------------------------------------------------------------------------------
class InstitutionOfferSerializer(serializers.ModelSerializer):
    offer=SerializerMethodField()
    def get_offer(self,obj):
        if obj.offer:
            return obj.offer.name

    class Meta:
            model = InstitutionOffer
            fields = ("id","offer",)

class InstitutionSerializer(serializers.ModelSerializer):
    offer_institution=InstitutionOfferSerializer(many=True)

    class Meta:
        model = Institution
        fields = "__all__"

class InstitutionalTypeserializer(serializers.ModelSerializer):
    social_user = SocialInstituionalSerializer(many=True)
    institution_user = InstitutionSerializer(many=True)
    class Meta:
        model = MyUser
        fields = ('uuid','email','user_type','social_user','institution_user',)

#------------------------------------------------------------------------------------
class ArtistAndProfessionalBioSerializer(serializers.ModelSerializer):
    def create(self, validated_data):

        params = self.context.get('params')
        bio,created =Bio.objects.get_or_create(user=validated_data['user'])
        if created:
            bio.stats_type=params['stats_type']
            bio.bio=params['bio']
        else:
            bio.stats_type=params['stats_type']
            bio.bio=params['bio']
        bio.save()
        if 'education' in params and params['education']:
            for data in params['education']:
                obj=Education.objects.create(name=data)
                BioEducation.objects.create(user=validated_data['user'],education=obj)
        return bio  
    class Meta:
        model = Bio
        fields = "__all__"

#------------------------------------------------------------------------------------
class AllUserMediaSerializer(serializers.ModelSerializer):
    def create(self, validated_data):
        params = self.context.get('params')
        mediaDetails=MediaDetails.objects.create(**validated_data)
        if 'media' in params:
            if isinstance(params['media'], list):
                for image in params['media']:
                    Media.objects.create(user=validated_data['user'],image=image)
            else:
                Media.objects.create(user=validated_data['user'],image=params['media'])
        return mediaDetails

    class Meta:
        model = MediaDetails
        fields = "__all__"

class UserAddWorkSerializer(serializers.ModelSerializer):
    def create(self, validated_data):
        params = self.context.get('params')
        addUserWork=AddUserWork.objects.create(**validated_data)

        if 'media' in params:
            if isinstance(params['media'], list):
                for image in params['media']:
                    instance=VideoAndImage.objects.create(image=image)
                    AddMediaInWork.objects.create(user=validated_data['user'],image=instance)
                    
            else:
                instance=VideoAndImage.objects.create(image=params['media'])
                AddMediaInWork.objects.create(user=validated_data['user'],image=instance)

        return addUserWork

    class Meta:
        model = AddUserWork
        fields = "__all__"

class UserAddProjectSerializer(serializers.ModelSerializer):
    def create(self, validated_data):
        params = self.context.get('params')
        addUserProject=AddUserProject.objects.create(**validated_data)

        if 'media' in params:
            if isinstance(params['media'], list):
                for image in params['media']:
                    instance=VideoAndImage.objects.create(image=image)
                    AddMediaInProject.objects.create(user=validated_data['user'],image=instance)
            else:
                instance=VideoAndImage.objects.create(image=params['media'])
                AddMediaInProject.objects.create(user=validated_data['user'],image=instance)
        return addUserProject

    class Meta:
        model = AddUserProject
        fields = "__all__"

class InstitutionInfoServiceSerializer(serializers.ModelSerializer):
    def create(self, validated_data):
        params = self.context.get('params')
        institutionInformation=InstitutionInformation.objects.create(**validated_data)
        if 'service' in params:
            for data in params['service']:
                serviceInstance=UserService.objects.get(id=data)
                instance,created = AddUserService.objects.get_or_create(
                    user=validated_data['user'],
                    service=serviceInstance
                )
        if 'activity' in params:
            for data in params['activity']:
                activity=Activity.objects.get(id=data)
                instance,created = InstitutionActivity.objects.get_or_create(
                    user=validated_data['user'],
                    activity=activity
                )
        return institutionInformation

    class Meta:
        model = InstitutionInformation
        fields = "__all__"

#---------------------------GetProfileByIdSerializer------------------------------
class GetBioSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Bio
        exclude = ("user",)

class GetEducationSerializer(serializers.ModelSerializer):
    education=SerializerMethodField()

    def get_education(self,obj):
        if obj:
            return obj.education.name

    class Meta:
        model = BioEducation
        exclude = ("user",)

class GetBioMediaSerializer(serializers.ModelSerializer):
    image = SerializerMethodField()
    def get_image(self,obj):
        if obj:
            return obj.image.url

    class Meta:
        model = BiographyLink
        exclude = ("user",)

class GetArtistInterest(serializers.ModelSerializer):
    user_interest=SerializerMethodField()

    def get_user_interest(self,obj):
        if obj:
            return obj.user_interest.name
    class Meta:
        model = ArtistUserInterest
        exclude = ("user",)

class GetArtistSkill(serializers.ModelSerializer):
    user_skill=SerializerMethodField()

    def get_user_skill(self,obj):
         if obj:
             return obj.user_skill.name

    class Meta:
        model = ArtistUserSkill
        exclude = ("user",)

class ArtistGetProfileByIdSerializer(serializers.ModelSerializer):
    bio_user = GetBioSerializer(many=True)
    bio_education_user = GetEducationSerializer(many=True)
    media_user = GetBioMediaSerializer(many=True)
    artist_interest_user = GetArtistInterest(many=True)
    artist_skill_user = GetArtistSkill(many=True)

    class Meta:
        model = MyUser
        exclude = ('password', 'last_login', 'updated_at', 'otp',
                   'is_superuser', 'is_staff', 'created_at',
                   'groups', 'user_permissions', 'deleted_at','is_otp_verified','is_active',"is_forgetpassword",)
#---------------------------------------------------------------------------------------
class GetExhibitionSerializer(serializers.ModelSerializer):

    class Meta:
        model = ArtistExhibitions
        exclude = ("user",)

class GetAchievementSerializer(serializers.ModelSerializer):

    class Meta:
        model = ArtistAchievement
        exclude = ("user",)

class GetPlaceSerializer(serializers.ModelSerializer):

    class Meta:
        model = Place
        exclude = ("user",)

class GetSaleSerializer(serializers.ModelSerializer):

    class Meta:
        model = ArtistSales
        exclude = ("user",)

class ArtistGetProfileByExperienceSerializer(serializers.ModelSerializer):
    artist_exhibition = GetExhibitionSerializer(many=True)
    artist_achievement = GetAchievementSerializer(many=True)
    place_user = GetPlaceSerializer(many=True)
    artist_sales = GetSaleSerializer(many=True)

    class Meta:
        model = MyUser
        exclude = ('password', 'last_login', 'updated_at', 'otp',
                   'is_superuser', 'is_staff', 'created_at',
                   'groups', 'user_permissions', 'deleted_at','is_otp_verified','is_active',"is_forgetpassword",)

#-----------------------------------------------------------------------------------------------------------
class GetWorkSerializer(serializers.ModelSerializer):
    thumbnail = SerializerMethodField()

    def get_thumbnail(self,obj):
        if obj:
            return obj.thumbnail.url

    class Meta:
        model = AddUserWork
        exclude = ("user",)

class GetMediaSerializer(serializers.ModelSerializer):
    image = SerializerMethodField()

    def get_image(self,obj):
        if obj:
            return obj.image.image.url

    class Meta:
        model = AddMediaInWork
        exclude = ("user",)

class ArtistGetProfileByWorkSerializer(serializers.ModelSerializer):
    add_user_work = GetWorkSerializer(many=True)
    user_add_media_work = GetMediaSerializer(many=True)

    class Meta:
        model = MyUser
        exclude = ('password', 'last_login', 'updated_at', 'otp',
                   'is_superuser', 'is_staff', 'created_at',
                   'groups', 'user_permissions', 'deleted_at','is_otp_verified','is_active',"is_forgetpassword",)
#-------------------------------------------------------------------------------------------------------------------
class GetAddServiceSerializer(serializers.ModelSerializer):
    service = SerializerMethodField()

    def get_service(slef,obj):
        if obj:
            return obj.service.name

    class Meta:
        model = AddUserService
        exclude = ("user",)

class ProfessionalGetProfileByIdSerializer(serializers.ModelSerializer):
    bio_user = GetBioSerializer(many=True)
    bio_education_user = GetEducationSerializer(many=True)
    media_user = GetBioMediaSerializer(many=True)
    add_user_service = GetAddServiceSerializer(many=True)

    class Meta:
        model = MyUser
        exclude = ('password', 'last_login', 'updated_at', 'otp',
                   'is_superuser', 'is_staff', 'created_at',
                   'groups', 'user_permissions', 'deleted_at','is_otp_verified','is_active',"is_forgetpassword",)

#---------------------------ProfessionalGetProfileByExperienceSerializer-------------------------------------------
class GetClientSerializer(serializers.ModelSerializer):

    class Meta:
        model = AddClient
        exclude = ("user",)

class GetAddArtistSerializer(serializers.ModelSerializer):
    artist =SerializerMethodField()

    def get_artist(self,obj):
        if obj:
            return obj.artist.name
    class Meta:
        model = ArtistAdd
        exclude = ("user",)

class GetAddProjectSerializer(serializers.ModelSerializer):

    class Meta:
        model = UserProject
        exclude = ("user",)  
        
class ProfessionalGetProfileByExperienceSerializer(serializers.ModelSerializer):
    place_user = GetPlaceSerializer(many=True)
    add_client_user = GetClientSerializer(many=True)
    add_artist = GetAddArtistSerializer(many=True)
    user_project = GetAddProjectSerializer(many=True)

    class Meta:
        model = MyUser
        exclude = ('password', 'last_login', 'updated_at', 'otp',
                   'is_superuser', 'is_staff', 'created_at',
                   'groups', 'user_permissions', 'deleted_at','is_otp_verified','is_active',"is_forgetpassword",)

#----------------------------ProfessionalGetProfileByWorkSerializer-------------------------------------------------
class ProfessionalGetProfileByWorkSerializer(serializers.ModelSerializer):
    add_user_work = GetWorkSerializer(many=True)
    user_add_media_work = GetMediaSerializer(many=True)

    class Meta:
        model = MyUser
        exclude = ('password', 'last_login', 'updated_at', 'otp',
                   'is_superuser', 'is_staff', 'created_at',
                   'groups', 'user_permissions', 'deleted_at','is_otp_verified','is_active',"is_forgetpassword",)


#----------------------InstitutionGetProfileByIdSerializer-------------------------------------------------------
class GetAddActivitySerializer(serializers.ModelSerializer):
    activity =SerializerMethodField()

    def get_activity(self,obj):
        if obj:
            return obj.activity.name

    class Meta:
        model = InstitutionActivity
        exclude = ("user",)  

class GetInformationSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = InstitutionInformation
        exclude = ("user",) 

class InstitutionGetProfileByIdSerializer(serializers.ModelSerializer):
    information_user = GetInformationSerializer(many=True)
    add_user_service = GetAddServiceSerializer(many=True)
    activity_user = GetAddActivitySerializer(many=True)
    
    class Meta:
        model = MyUser
        exclude = ('password', 'last_login', 'updated_at', 'otp',
                   'is_superuser', 'is_staff', 'created_at',
                   'groups', 'user_permissions', 'deleted_at','is_otp_verified','is_active',"is_forgetpassword",)

#---------------------------------InstitutionGetProfileByExperienceSerializer------------------------------------------

class GetAddBrandSerializer(serializers.ModelSerializer):
    brand = SerializerMethodField()

    def get_brand(self,obj):
        if obj:
            return obj.brand.name

    class Meta:
        model = AddBrand
        exclude = ("user",) 

class InstitutionGetProfileByExperienceSerializer(serializers.ModelSerializer):
    user_project = GetAddProjectSerializer(many=True)
    add_artist = GetAddArtistSerializer(many=True)
    place_user = GetPlaceSerializer(many=True)
    add_brand_user = GetAddBrandSerializer(many=True)

    class Meta:
        model = MyUser
        exclude = ('password', 'last_login', 'updated_at', 'otp',
                   'is_superuser', 'is_staff', 'created_at',
                   'groups', 'user_permissions', 'deleted_at','is_otp_verified','is_active',"is_forgetpassword",)

class GetArtistImageSerializer(serializers.ModelSerializer):
    work_image = SerializerMethodField()

    def get_work_image(self,obj):
        if obj:
            return obj.work_image.url
    class Meta:
        model = Artist
        fields="__all__"

class ArtistImageSerializer(serializers.ModelSerializer):
    artist_user = GetArtistImageSerializer(many=True)

    class Meta:
        model = MyUser
        exclude = ('password', 'last_login', 'updated_at', 'otp',
                   'is_superuser', 'is_staff', 'created_at',
                   'groups', 'user_permissions', 'deleted_at','is_otp_verified','is_active',"is_forgetpassword","dob","social_id")

   