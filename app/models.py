import jwt
import uuid
import pyotp
from rest_framework_jwt.utils import jwt_payload_handler
from django.db import models
from django.conf import settings
from cloudinary.models import CloudinaryField as BaseCloudinaryField
from djrichtextfield.models import RichTextField
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser,PermissionsMixin

# Create your models here.
class CloudinaryField(BaseCloudinaryField):
    def upload_options(self, model_instance):
        return {
        'resource_type':'raw',
        }


class MyUserManager(BaseUserManager):
    ''' Inherits BaseUserManager class'''

    def create_superuser(self, email, password):
        '''Creates and saves a superuser with the given email and password.'''
        user = self.model(email=email)
        user.set_password(password)
        user.is_superuser = True
        user.is_active = True
        user.is_staff = True
        user.save(using=self._db)
        return user


# --------------Model for website User--------------------

class MyUser(AbstractBaseUser, PermissionsMixin):
    '''Base User Table used same for Authentication Purpose	'''
    '''Docstring for MyUser'''
    GENDER = (
        ('Male', 'Male'),
        ('Female', 'Female'),
    )
    USER_TYPE = (
        ('Artist', 'Artist'),
        ('Professional', 'Professional'),
        ('Institution', 'Institution'),
    )

    uuid = models.UUIDField(
        default=uuid.uuid4,editable=False,unique=True
    )
    social_id = models.CharField(
        "Social id",max_length=100,blank=True,null=True,
    )
    email = models.EmailField(
        "Email",unique=True,max_length=255
    )
    user_name = models.CharField(
        "User Name",max_length=100,blank=True,null=True,
    )
    name = models.CharField(
        "Name",max_length=100,blank=True,null=True
    )
    gender = models.CharField(
        "Gender",
        max_length=10,choices=GENDER,blank=True,null=True
    )
    age = models.CharField(
        "Age",max_length=50, blank=True, null=True
    )
    user_type = models.CharField(
        "user_type",max_length=30,choices=USER_TYPE,default='Registered user'
    )
    country = models.CharField(
        "Country", max_length=100, blank=True, null=True
    )
    dob = models.CharField(
        "Dob", max_length=100, blank=True, null=True
    )
    otp = models.CharField("Otp", blank=True,
                           null=True, max_length=10
                           )
    is_otp_verified = models.BooleanField(
        'Otp Verified', default=False
    )
    image = CloudinaryField(null=True,blank=True)
    is_forgetpassword = models.BooleanField(
        'Forgot Link Request', default=False
    )
    is_active = models.BooleanField(
        'Active',default=False
    )
    is_staff = models.BooleanField(
        'Staff', default=False
    )
    created_at = models.DateTimeField(
        auto_now_add=True
    )
    updated_at = models.DateTimeField(
        auto_now=True
    )
    deleted_at = models.DateTimeField(
        blank=True,null=True
    )

    objects = MyUserManager()
    USERNAME_FIELD = 'email'

    def __str__(self):
        return self.email

    def get_short_name(self):
        return self.first_name

    def create_jwt(self):
        """Function for creating JWT for Authentication Purpose"""
        payload = jwt_payload_handler(self)
        token = jwt.encode(payload, settings.SECRET_KEY)
        auth_token = token.decode('unicode_escape')
        return auth_token

    def otp_creation(self):
        totp = pyotp.TOTP("JBSWY3DPEHPK3PXP", digits=4)
        otp = totp.now()
        self.otp = otp
        self.save()
        return otp

    def otp_Verification(self,otp):
        """Otp Verification Function"""
        if self.otp==otp:
            self.otp_creation()
            return True
        return False

    class Meta:
        '''docstring for meta'''
        verbose_name_plural = "User"


# -------------------------------------Intrest/Goal/Artist/ArtistIntrest/ArtistGoal-------------------------
class Interest(models.Model):
    '''model for Intrest'''
    name = models.CharField(
        "Name", max_length=100, blank=True, null=True
    )

    def __str__(self):
        return self.name

    class Meta:
        '''docstring for meta'''
        verbose_name_plural = "Signup Interest"


class Goal(models.Model):
    '''model for Goal'''
    name = models.CharField(
        "Name", max_length=100, blank=True, null=True
    )

    def __str__(self):
        return self.name

    class Meta:
        '''docstring for meta'''
        verbose_name_plural = "Signup Goal"


class Artist(models.Model):
    '''model for Artist'''
    artist_type = (
        ('Full time artist', 'Full time artist'),
        ('Another day job', 'Another day job'),
    )
    user = models.ForeignKey(
        MyUser,
        on_delete=models.CASCADE, related_name="artist_user"
    )
    carrer = models.CharField(
        "Carrer", max_length=100, blank=True, null=True
    )

    organisation = models.CharField(
        "Organisation ", max_length=100, blank=True, null=True
    )
    job_type = models.CharField(
        "Artist Type",
        max_length=100, choices=artist_type, blank=True, null=True
    )
    contact_email = models.EmailField(
        "Email", max_length=255
    )
    messenger = models.CharField(
        "Messenger", max_length=100, blank=True, null=True,
    )
    agent_gallery = models.URLField("Agent or Gallery", max_length=250)
    work_image = CloudinaryField(null=True, blank=True)

    def __str__(self):
        return str(self.user.email)

    class Meta:
        '''docstring for meta'''
        verbose_name_plural = "Artist"


class ArtistInterest(models.Model):
    '''model for ArtistIntrest'''
    artist = models.ForeignKey(
        Artist,
        on_delete=models.CASCADE, related_name="artist_interest"
    )
    interest = models.ForeignKey(
        Interest,
        on_delete=models.CASCADE, related_name="interest"
    )

    class Meta:
        '''docstring for meta'''
        verbose_name_plural = "Artist Interest"


class ArtistGoal(models.Model):
    '''model for Artist Goal'''
    artist = models.ForeignKey(
        Artist,
        on_delete=models.CASCADE, related_name="artist_goal"
    )
    goal = models.ForeignKey(
        Goal,
        on_delete=models.CASCADE, related_name="goal"
    )

    class Meta:
        '''docstring for meta'''
        verbose_name_plural = "Artist Goal"


# --------------------------Service/Professional/ProfessionalServices/ProfessionalGoal-----------------------
class Service(models.Model):
    '''model for Service'''
    name = models.CharField(
        "Name", max_length=100, blank=True, null=True
    )

    def __str__(self):
        return self.name

    class Meta:
        '''docstring for meta'''
        verbose_name_plural = "Signup Service"


class Professional(models.Model):
    '''model for Professional'''
    professional_type = (
        ('Work for', 'Work for'),
        ('Self employee', 'Self employee'),
    )
    user = models.ForeignKey(
        MyUser,
        on_delete=models.CASCADE, related_name="professional_user"
    )
    artistic_profession = models.CharField(
        "Artistic Profession", max_length=100, blank=True, null=True
    )

    job_type = models.CharField(
        "Professional Type",
        max_length=100, choices=professional_type, blank=True, null=True
    )
    organisation = models.CharField(
        "Organisation ", max_length=100, blank=True, null=True
    )

    def __str__(self):
        return str(self.user.email)

    class Meta:
        '''docstring for meta'''
        verbose_name_plural = "Professional"


class ProfessionalServices(models.Model):
    '''model for Professional Services'''
    professional = models.ForeignKey(
        Professional,
        on_delete=models.CASCADE, related_name="professional_service"
    )
    service = models.ForeignKey(
        Service,
        on_delete=models.CASCADE, related_name="service"
    )

    class Meta:
        '''docstring for meta'''
        verbose_name_plural = "Professional Services"


class ProfessionalGoal(models.Model):
    '''model for Professional Goal'''
    professional = models.ForeignKey(
        Professional,
        on_delete=models.CASCADE, related_name="professional_goal"
    )
    goal = models.ForeignKey(
        Goal,
        on_delete=models.CASCADE, related_name="goal_professional"
    )

    class Meta:
        '''docstring for meta'''
        verbose_name_plural = "Professional Goal"


# ------------------------------------Institution/Offer/InstitutionOffer-----------------------------------
class Offer(models.Model):
    '''model for Offer'''
    name = models.CharField(
        "Name", max_length=100, blank=True, null=True
    )

    def __str__(self):
        return self.name

    class Meta:
        '''docstring for meta'''
        verbose_name_plural = "Signup Offer"


class Institution(models.Model):
    '''model for Institution'''
    user = models.ForeignKey(
        MyUser,
        on_delete=models.CASCADE, related_name="institution_user"
    )
    institution_type = models.CharField(
        "Institution Type ", max_length=100, blank=True, null=True
    )
    institution_category = models.CharField(
        "Institution Category", max_length=100, blank=True, null=True
    )
    location = models.CharField(
        "Location", max_length=100, blank=True, null=True
    )
    logo = CloudinaryField(null=True, blank=True)

    class Meta:
        '''docstring for meta'''
        verbose_name_plural = "Institution"

    def __str__(self):
            return str(self.user.email)

class InstitutionOffer(models.Model):
    '''model for Institution Offer'''
    institution = models.ForeignKey(
        Institution,
        on_delete=models.CASCADE, related_name="offer_institution"
    )
    offer = models.ForeignKey(
        Offer,
        on_delete=models.CASCADE, related_name="offer"
    )

    class Meta:
        '''docstring for meta'''
        verbose_name_plural = "Institution Offer"


# -----------------------------SOCIAL----------------------------------------------------------------------
class Social(models.Model):
    '''model for Offer'''
    user = models.ForeignKey(
        MyUser,
        on_delete=models.CASCADE, related_name="social_user"
    )
    website = models.URLField("Website", max_length=250)
    instagram = models.URLField("Instagram", max_length=250)
    facebook = models.URLField("Facebook", max_length=250)
    youtube = models.URLField("Youtube", max_length=250)

    class Meta:
        '''docstring for meta'''
        verbose_name_plural = "Social"
    def __str__(self):
        return str(self.user.email)


# -----------------------------Blog----------------------------------------------------------------------
class Blog(models.Model):
    """Model of Blog"""
    user = models.ForeignKey(
        MyUser,
        on_delete=models.CASCADE, related_name="blog_user"
    )
    title = models.CharField(
        "Title", max_length=100, blank=True, null=True
    )
    description = RichTextField("Description", blank=True, null=True)
    blog_image = CloudinaryField("Blog Image", null=True, blank=True)
    created_at = models.DateTimeField(
        auto_now_add=True
    )
    updated_at = models.DateTimeField(
        auto_now=True
    )
    deleted_at = models.DateTimeField(
        blank=True, null=True
    )

    class Meta:
        '''docstring for meta'''
        verbose_name_plural = "Blog"

    def __str__(self):
        return str(self.user.email)


class Comment(models.Model):
    user = models.ForeignKey(
        MyUser,
        on_delete=models.CASCADE, related_name="comment_user"
    )
    blog = models.ForeignKey(
        Blog,
        on_delete=models.CASCADE, related_name="blog"
    )
    comment = models.CharField(
        "Comment", max_length=300, blank=True, null=True
    )
    created_at = models.DateTimeField(
        auto_now_add=True, blank=True, null=True
    )
    updated_at = models.DateTimeField(
        auto_now=True, blank=True, null=True
    )
    deleted_at = models.DateTimeField(
        blank=True, null=True
    )
    def __str__(self):
        return str(self.user.email)
    class Meta:
        '''docstring for meta'''
        verbose_name_plural = "Comment"

# --------------------------------------------Follow------------------------------------------------------------------
class Follow(models.Model):
    user = models.ForeignKey(
        MyUser,
        on_delete=models.CASCADE, related_name="follow_user"
    )
    to_follower=models.ForeignKey(
        MyUser,
        on_delete=models.CASCADE, related_name="to_follow"
    )
    is_follow=models.BooleanField(
        'Follow', default=True
    )
    created_at = models.DateTimeField(
        auto_now_add=True, blank=True, null=True
    )
    def __str__(self):
        return str(self.user.email)
    class Meta:
        '''docstring for meta'''
        verbose_name_plural = "Follow"

# ----------------------------------------------------Connect------------------------------------------------------
class Connect(models.Model):
    user = models.ForeignKey(
        MyUser,
        on_delete=models.CASCADE, related_name="connect_user"
    )
    connect=models.ForeignKey(
        MyUser,
        on_delete=models.CASCADE, related_name="to_connect"
    )
    is_connect=models.BooleanField(
        'Connect', default=True
    )
    created_at = models.DateTimeField(
        auto_now_add=True, blank=True, null=True
    )
    
    def __str__(self):
        return str(self.user.email)
    class Meta:
        '''docstring for meta'''
        verbose_name_plural = "Connect"

# -----------------------------Photos----------------------------------------------------------------------
class Photos(models.Model):
    user = models.ForeignKey(
        MyUser,
        on_delete=models.CASCADE, related_name="photo_user"
    )
    title = models.CharField(
        "Title",max_length=100,blank=True,null=True
    )
    image = CloudinaryField(null=True,blank=True)

    created_at = models.DateTimeField(
        auto_now_add=True
    )
    def __str__(self):
        return str(self.user.email)

    class Meta:
        '''docstring for meta'''
        verbose_name_plural = "Photo"

# -----------------------------Gallery----------------------------------------------------------------------
class Gallery(models.Model):
    user = models.ForeignKey(
        MyUser,
        on_delete=models.CASCADE, related_name="gallery_user"
    )
    title = models.CharField(
        "Title",max_length=100,blank=True,null=True
    )
    image = CloudinaryField(null=True,blank=True)

    created_at = models.DateTimeField(
        auto_now_add=True
    )
    def __str__(self):
        return str(self.user.email)

    class Meta:
        '''docstring for meta'''
        verbose_name_plural = "Gallery"

# -----------------------------Education----------------------------------------------------------------------
class Education(models.Model):
    '''model for User Interest'''

    name = models.CharField(
        "Name",max_length=100,blank=True,null=True
    )
    def __str__(self):
        return self.name

    class Meta:
        '''docstring for meta'''
        verbose_name_plural = "Education"

# -----------------------------Bio----------------------------------------------------------------------
class BiographyLink(models.Model):
    user = models.ForeignKey(
        MyUser,
        on_delete=models.CASCADE, related_name="media_user"
    )
    image = CloudinaryField(null=True,blank=True)
    

    def __str__(self):
        return str(self.user.email)

    class Meta:
        '''docstring for meta'''
        verbose_name_plural = "Biography Link"


class BioEducation(models.Model):
    user = models.ForeignKey(
        MyUser,
        on_delete=models.CASCADE, related_name="bio_education_user"
    )
    education = models.ForeignKey(
        Education,
        on_delete=models.CASCADE, related_name="education"
    )
    
    def __str__(self):
        return str(self.user.email)

    class Meta:
        '''docstring for meta'''
        verbose_name_plural = "Bio Education"


class Bio(models.Model):
    stats= (
        ('Full Time','Full Time'),
        ('Part Time','Part Time'),
    )
    user = models.ForeignKey(
        MyUser,
        on_delete=models.CASCADE, related_name="bio_user"
    )
    
    bio = models.CharField(
        "Bio",max_length=100,blank=True,null=True
    )
    stats_type = models.CharField(
        "Stats Type",
        max_length=100, choices=stats, blank=True, null=True
    )

    def __str__(self):
        return str(self.user.email)

    class Meta:
        '''docstring for meta'''
        verbose_name_plural = "Bio"

#-----------------------------Project-----------------------------------
class Project(models.Model):
    user = models.ForeignKey(
        MyUser,
        on_delete=models.CASCADE, related_name="project_user"
    )
    title = models.CharField(
        "Title",max_length=100,blank=True,null=True
    )
    image = CloudinaryField(null=True,blank=True
    )
    is_active = models.BooleanField(
        'Active',default=True
    )
    created_at = models.DateTimeField(
        auto_now_add=True
    )
    amount = models.CharField(
        "Amount",max_length=100,blank=True,null=True
    )
    description = models.CharField(
        "Description",max_length=250,blank=True,null=True
    )
    rules = models.CharField(
        "Rules",max_length=250,blank=True,null=True
    )
    def __str__(self):
        return str(self.user.email)

    class Meta:
        '''docstring for meta'''
        verbose_name_plural = "Project"

#---------------------Rating-----------------------------------------
class Rating(models.Model):
    user = models.ForeignKey(
        MyUser,
        on_delete=models.CASCADE, related_name="rating_user"
    )
    to_rate =models.ForeignKey(
        MyUser,
        on_delete=models.CASCADE, related_name="to_rate"
    )
    rating = models.IntegerField(
        "Rating",default=1
    )
    def __str__(self):
        return str(self.user.email)

    class Meta:
        '''docstring for meta'''
        verbose_name_plural = 'Rating'

#------------------User Skill/Interest---------------------------------------------
class UserSkill(models.Model):
    '''model for User Skill'''
    name = models.CharField(
        "Name",max_length=100,blank=True,null=True
    )
    def __str__(self):
        return self.name

    class Meta:
        '''docstring for meta'''
        verbose_name_plural = "User Skill"


class UserInterest(models.Model):
    '''model for User Interest'''
    name = models.CharField(
        "Name",max_length=100,blank=True,null=True
    )
    def __str__(self):
        return self.name

    class Meta:
        '''docstring for meta'''
        verbose_name_plural = "User Interest"

#---------------------Artist User skill------------------------------------------------
class ArtistUserSkill(models.Model):
    user = models.ForeignKey(
        MyUser,
        on_delete=models.CASCADE, related_name="artist_skill_user"
    )
    user_skill = models.ForeignKey(
        UserSkill,
        on_delete=models.CASCADE, related_name="user_skill"
    )

    class Meta:
        '''docstring for meta'''
        verbose_name_plural = "Artist User Skill"


class ArtistUserInterest(models.Model):
    user = models.ForeignKey(
        MyUser,
        on_delete=models.CASCADE, related_name="artist_interest_user"
    )
    user_interest = models.ForeignKey(
        UserInterest,
        on_delete=models.CASCADE, related_name="user_interest"
    )

    class Meta:
        '''docstring for meta'''
        verbose_name_plural = "Artist User Interest"
#-----------------------Artist Achievement-------------------------------
class ArtistAchievement(models.Model):
    user = models.ForeignKey(
        MyUser,
        on_delete=models.CASCADE, related_name="artist_achievement"
    )
    achievement = models.CharField(
        "Achievement",max_length=100,blank=True,null=True
    )
    no=models.CharField(
        "Number",max_length=100,blank=True,null=True
    )

    class Meta:
        '''docstring for meta'''
        verbose_name_plural = "Artist Achievement"

#-----------------------Artist Exhibitions--------------------------------
class ArtistExhibitions(models.Model):
    user = models.ForeignKey(
        MyUser,
        on_delete=models.CASCADE, related_name="artist_exhibition"
    )
    exhibitions = models.CharField(
        "Exhibitions",max_length=100,blank=True,null=True
    )
    no=models.CharField(
        "Number",max_length=100,blank=True,null=True
    )

    class Meta:
        '''docstring for meta'''
        verbose_name_plural = "Artist Exhibitions"


#----------------------------------Artist Sales---------------------------------------
class ArtistSales(models.Model):
    user = models.ForeignKey(
        MyUser,
        on_delete=models.CASCADE, related_name="artist_sales"
    )
    sales = models.CharField(
        "Number",max_length=100,blank=True,null=True
    )
    def __str__(self):
        return str(self.user.email)

    class Meta:
        '''docstring for meta'''
        verbose_name_plural = "Artist Sales"

#------------------------------Add Artist-------------------------------------------------
class ArtistAdd(models.Model):
    user = models.ForeignKey(
        MyUser,
        on_delete=models.CASCADE, related_name="add_artist"
    )
    artist = models.ForeignKey(
       MyUser,
        on_delete=models.CASCADE, related_name="artist"
    )
    def __str__(self):
        return str(self.user.email)

    class Meta:
        '''docstring for meta'''
        verbose_name_plural = "Add Artist"

#----------------------User Service----------------------------------------------------
class UserService(models.Model):
    '''model for User Interest'''
    name = models.CharField(
        "Name",max_length=100,blank=True,null=True
    )
    def __str__(self):
        return self.name

    class Meta:
        '''docstring for meta'''
        verbose_name_plural = "User Services"

class AddUserService(models.Model):
    user = models.ForeignKey(
        MyUser,
        on_delete=models.CASCADE, related_name="add_user_service"
    )
    service = models.ForeignKey(
        UserService,
        on_delete=models.CASCADE, related_name="add_service"
    )

    def __str__(self):
        return str(self.user.email)

    class Meta:
        '''docstring for meta'''
        verbose_name_plural = "Add User Service"

#----------------------User Service----------------------------------------------------
# class JobRole(models.Model):
#     '''model for User Interest'''
#     name = models.CharField(
#         "Name",max_length=100,blank=True,null=True
#     )
#     def __str__(self):
#         return self.name

#     class Meta:
#         '''docstring for meta'''
#         verbose_name_plural = "Job Role"

# class AddJobRole(models.Model):
#     user = models.ForeignKey(
#         MyUser,
#         on_delete=models.CASCADE, related_name="add_job_user"
#     )
#     job_role = models.ForeignKey(
#         JobRole,
#         on_delete=models.CASCADE, related_name="add_job_role"
#     )

#     class Meta:
#         '''docstring for meta'''
#         verbose_name_plural = "Add Job Role"


#----------------------User Service----------------------------------------------------
class AddClient(models.Model):
    user = models.ForeignKey(
        MyUser,
        on_delete=models.CASCADE, related_name="add_client_user"
    )
    client = models.CharField(
        "Client",max_length=100,blank=True,null=True
    )
    def __str__(self):
        return str(self.user.email)

    class Meta:
        '''docstring for meta'''
        verbose_name_plural = "Add Client"

#-------------------------Team----------------------------------------------------------
class AddTeam(models.Model):
    user = models.ForeignKey(
        MyUser,
        on_delete=models.CASCADE, related_name="add_team_user"
    )
    team = models.ForeignKey(
        MyUser,
        on_delete=models.CASCADE, related_name="add_team"
    )

    class Meta:
        '''docstring for meta'''
        verbose_name_plural = "Add Team"
#-----------------------------------------------------------------------------------
class Place(models.Model):
    user = models.ForeignKey(
        MyUser,
        on_delete=models.CASCADE, related_name="place_user"
    )

    place= models.CharField(
        "Name",max_length=100,blank=True,null=True
    )

    def __str__(self):
        return str(self.user.email)

    class Meta:
        '''docstring for meta'''
        verbose_name_plural = "Place"
#-------------------------Brand/Endorsed By----------------------------------------------------------
class Brand(models.Model):
    '''model for User Interest'''
    name = models.CharField(
        "Name",max_length=100,blank=True,null=True
    )
    def __str__(self):
        return self.name

    class Meta:
        '''docstring for meta'''
        verbose_name_plural = "Brand"

class AddBrand(models.Model):
    user = models.ForeignKey(
        MyUser,
        on_delete=models.CASCADE, related_name="add_brand_user"
    )
    brand= models.ForeignKey(
        Brand,
        on_delete=models.CASCADE, related_name="add_brand"
    )
    def __str__(self):
        return str(self.user.email)

    class Meta:
        '''docstring for meta'''
        verbose_name_plural = "Endorsed By"

#-------------------------Activity---------------------------------------------------------------------
class Activity(models.Model):
    '''model for User Interest'''
    name = models.CharField(
        "Name",max_length=100,blank=True,null=True
    )
    def __str__(self):
        return self.name

    class Meta:
        '''docstring for meta'''
        verbose_name_plural = "Activity"

#----------------------------Institution Information---------------------------------------------------
class InstitutionActivity(models.Model):
    user = models.ForeignKey(
        MyUser,
        on_delete=models.CASCADE, related_name="activity_user"
    )
    activity = models.ForeignKey(
        Activity,
        on_delete=models.CASCADE, related_name="activity"
    )
class InstitutionInformation(models.Model):
    user = models.ForeignKey(
        MyUser,
        on_delete=models.CASCADE, related_name="information_user"
    )
   
    information = models.CharField(
        "Information",max_length=100,blank=True,null=True
    )
    def __str__(self):
        return str(self.user.email)

    class Meta:
        '''docstring for meta'''
        verbose_name_plural = "Institution Information"

# --------------------------Media----------------------------------------------------------------------
class Media(models.Model):
    '''model for User Interest'''
    user = models.ForeignKey(
        MyUser,
        on_delete=models.CASCADE, related_name="user_media"
    )
    image = CloudinaryField(
        null=True,blank=True
        )
    def __str__(self):
        return str(self.user)

    class Meta:
        '''docstring for meta'''
        verbose_name_plural = "Media"

class VideoAndImage(models.Model):
    '''model for User Interest'''
    image = CloudinaryField(
        null=True,blank=True
        )

    class Meta:
        '''docstring for meta'''
        verbose_name_plural = "Video And Image"      

class AddMediaInProject(models.Model):
    user = models.ForeignKey(
        MyUser,
        on_delete=models.CASCADE, related_name="user_add_media_projecct"
    )
    image = models.ForeignKey(
        VideoAndImage,
        on_delete=models.CASCADE, related_name="video_image_project"
    )
    def __str__(self):
        return str(self.user)

    class Meta:
        '''docstring for meta'''
        verbose_name_plural = "Add Media In Project"
    
class AddMediaInWork(models.Model):
    user = models.ForeignKey(
        MyUser,
        on_delete=models.CASCADE, related_name="user_add_media_work"
    )
    image = models.ForeignKey(
        VideoAndImage,
        on_delete=models.CASCADE, related_name="video_image_work"
    )
    def __str__(self):
        return str(self.user)

    class Meta:
        '''docstring for meta'''
        verbose_name_plural = "Add Media In Work"
    
class AddUserProject(models.Model):
    filter = (
        ('Active','Active'),
        ('Past','Past'),
    )
   
    user = models.ForeignKey(
        MyUser,
        on_delete=models.CASCADE, related_name="add_user_project"
    )
    
    status = models.CharField(
        "Status",
        max_length=100, choices=filter, blank=True, null=True
    )
    thumbnail = CloudinaryField(
        null=True,blank=True
    )
    image_title = models.CharField(
        "Image Title",max_length=100,blank=True,null=True
    )
    date = models.CharField(
        "Date", max_length=100, blank=True, null=True
    )
    description = models.CharField(
        "Description",max_length=255,blank=True,null=True
    )
    city = models.CharField(
        "City",max_length=100,blank=True,null=True
    )
    country = models.CharField(
        "Country",max_length=100,blank=True,null=True
    )
    collaborations = models.CharField(
        "Collaborations",max_length=100,blank=True,null=True
    )
    
    link = models.URLField(
        "Gallery Link", max_length=250
    )
    created_at = models.DateTimeField(
        auto_now_add=True
    )
    def __str__(self):
        return str(self.user)

    class Meta:
        '''docstring for meta'''
        verbose_name_plural = "Add User Project"

class AddUserWork(models.Model):
    filter = (
        ('Available','Available'),
        ('Sold','Sold'),
    )
    user = models.ForeignKey(
        MyUser,
        on_delete=models.CASCADE, related_name="add_user_work"
    )
    status = models.CharField(
        "Status",
        max_length=100, choices=filter, blank=True, null=True
    )
    thumbnail = CloudinaryField(
        null=True,blank=True
    )
    image_title = models.CharField(
        "Image Title",max_length=100,blank=True,null=True
    )
    size = models.CharField(
        "Size", max_length=100, blank=True, null=True
    )
    medium = models.CharField(
        "Medium",max_length=255,blank=True,null=True
    )
    year = models.CharField(
        "Year",max_length=100,blank=True,null=True
    )
    tag = models.CharField(
        "Tag",max_length=100,blank=True,null=True
    )
    created_at = models.DateTimeField(
        auto_now_add=True
    )
    def __str__(self):
        return str(self.user)

    class Meta:
        '''docstring for meta'''
        verbose_name_plural = "Add User Project"
#------------------------------------------------------------------------
class MediaDetails(models.Model):
    filter = (
        ('Exhibitions','Exhibitions'),
        ('Projects','Projects'),
        ('Press','Press'),
    )
    user = models.ForeignKey(
        MyUser,
        on_delete=models.CASCADE, related_name="user_media_details"
    )
    
    filter_type = models.CharField(
        "Filter Type",
        max_length=100, choices=filter, blank=True, null=True
    )
    thumbnail = CloudinaryField(
        null=True,blank=True
    )
    image_title = models.CharField(
        "Image Title",max_length=100,blank=True,null=True
    )
    city = models.CharField(
        "City",max_length=100,blank=True,null=True
    )
    country = models.CharField(
        "Country",max_length=100,blank=True,null=True
    )
    date = models.CharField(
        "Date", max_length=100, blank=True, null=True
    )
    gallery_link = models.URLField(
        "Gallery Link", max_length=250
    )
    created_at = models.DateTimeField(
        auto_now_add=True
    )
    def __str__(self):
        return str(self.user)

    class Meta:
        '''docstring for meta'''
        verbose_name_plural = "User Media"
#------------------------------------------------------
class UserProject(models.Model):

    user = models.ForeignKey(
        MyUser,
        on_delete=models.CASCADE, related_name="user_project"
    )
    project= models.CharField(
        "Project",max_length=100,blank=True,null=True
    )
    no=models.CharField(
        "Number",max_length=100,blank=True,null=True
    )

    class Meta:
        '''docstring for meta'''
        verbose_name_plural = "User Project"


class ReviewAndRating(models.Model):
    user = models.ForeignKey(
        MyUser,
        on_delete=models.CASCADE, related_name="user_review_rating"
    )
    to_rating = models.ForeignKey(
        MyUser,
        on_delete=models.CASCADE, related_name="to_rating"
    )
    review = models.CharField(
        "Review",max_length=250,blank=True,null=True
    )
    rating = models.IntegerField(
        "Rating",default=0
    )
    created_at = models.DateTimeField(
        auto_now_add=True
    )
    def __str__(self):
        return str(self.user.email)

    class Meta:
        '''docstring for meta'''
        verbose_name_plural = 'Review And Rating'

