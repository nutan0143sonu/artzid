# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import json

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated

from cloudinary.uploader import upload

from django.contrib.auth import authenticate ,login , logout

import datetime
from app.mail import *
from app.models import *
from app.serializers import *
from app.permissions import *
from django.db.models import Sum
from django.conf import settings


from django.core.mail import send_mail
from django.utils.encoding import force_bytes, force_text
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode


# --------------------------------------------------SingUp-------------------------------------------------
class SignUpView(APIView):
    """ 
    SignUp for Artist , Institution and Professional
    """
    def post(self, request):
        params = request.data
        print("PARAMS",params)
        data = {}
        try:
            user = MyUser.objects.get(email=params['email'])
            if user:
                return Response({"message": "Email id Allready Exist"
                }, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            print("Exception 1",e)
            try:
                if 'user_type' in params:
                    if params['user_type'] == 'Artist':
                        serializer = ArtistSignupSerializers(data=params, context={"params": params})
                        serializer.is_valid(raise_exception=True)
                        artistUser = serializer.save()
                        sendEmail(artistUser)
                        data = {
                            "data": serializer.data,
                        }
                    elif params['user_type'] == 'Institution':
                        serializer = InstitutionSignupSerializers(data=params, context={"params": params})
                        serializer.is_valid(raise_exception=True)
                        institutionUser = serializer.save()
                        sendEmail(institutionUser)
                        data = {
                            "data": serializer.data,
                        }
                    elif params['user_type'] == 'Professional':
                        serializer = ProfessionalSignupSerializers(data=params, context={"params": params})
                        serializer.is_valid(raise_exception=True)
                        professionalUser = serializer.save()
                        sendEmail(professionalUser)
                        data = {
                            "data": serializer.data,
                        }
                    else:
                        return Response({"message":"Invalid User Type"
                        }, status=status.HTTP_400_BAD_REQUEST)
                    return Response({"data":data,"message":"Data added successfully"}, status=status.HTTP_200_OK)
                return Response({"message":"User type is not in request"},status=status.HTTP_400_BAD_REQUEST)
            except Exception as e:
                print("Exception:",e)
                return Response(status=status.HTTP_400_BAD_REQUEST)
            
# --------------------------------------------------SingIn-------------------------------------------------
class LoginView(APIView):
    """ 
    SignIn for Artist , Institution and Professional,
    All user can signin from here.
    """
    def post(self, request):
        params = request.data
        print("PARAMS",params)
        try:
            myUser = MyUser.objects.get(email=params['email'])
            if myUser.is_otp_verified:
                user = authenticate(email=params['email'], password=params['password'])
                print(user)
                if user is not None:
                    login(request, user)
                    serializer = LoginSerializer(user)
                    return Response({"data": serializer.data,"message": "Logged In Successfully.","token": user.create_jwt()
                    },status=status.HTTP_200_OK)
                return Response({"message": "Invalid email or password"
                },status=status.HTTP_400_BAD_REQUEST)
            return Response({"message": "Please Verify OTP First."
                },status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            print("View Exception", e)
            return Response({"message": "Email Not Regisetered."
                },status=status.HTTP_400_BAD_REQUEST)

# ------------------------------OTP-Verified---------------------------------------------------------------
class OtpVerifyView(APIView):
    """
    Otp Verification
    """
    def post(self, request):
        params = request.data
        try:
            user = MyUser.objects.get(email=params['email'])
            if user.otp_Verification(params['otp']):
                user.is_otp_verified=True
                user.is_active=True
                user.save()
                return Response({"message": "Otp Verified Successfully."
                }, status=status.HTTP_200_OK)
            return Response({"message": "incorrect Otp."
            }, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            print("exception",e)
            return Response({"message": "Email Not Regisetered."
            }, status=status.HTTP_400_BAD_REQUEST)

# -----------------------------RE-Send Otp-----------------------------------------------------------------
class ResendOtpView(APIView):
    """
    Re Sent Otp 
    """
    def post(self, request):
        params = request.data
        try:
            user = MyUser.objects.get(email=params['email'])
            user.otp_creation()
            user.save()
            sendEmail(user)
            return Response({"message": "Otp Sent Successfully."
            }, status=status.HTTP_200_OK)
        except Exception as e:
            print("exception",e)
            return Response({"message": "Email Not Regisetered."
            }, status=status.HTTP_400_BAD_REQUEST)

class ForgotPasswordView(APIView):
    ''' View for forget password '''

    def post(self, request):
        params = request.data
        useremail = params['email']
        try:
            instance = MyUser.objects.get(email=useremail)
            subject = 'To reset your password use the link'
            uid = urlsafe_base64_encode(force_bytes(instance.uuid))
            time = urlsafe_base64_encode(force_bytes(datetime.datetime.now()))
            message = "http://" + str(get_current_site(request)) + "/reset-password/{0}/{1}".format(
                uid.decode('utf8'), time.decode('utf8'))
            send_mail(subject, message, from_email=settings.EMAIL_HOST_USER,
                      recipient_list=[instance.email], )
            return Response({"message": "Password reset link is sent to your email address."
            },status=status.HTTP_200_OK)
        except Exception as e:
            print("exception",e)
            return Response({"message": "Error in sending the reset link"
            }, status=status.HTTP_400_BAD_REQUEST)

class ResetPasswordGetView(APIView):
    ''' View for reset password '''

    def post(self, request, uidb64, time):
        from django.utils.dateparse import parse_datetime
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = MyUser.objects.get(uuid=uid)
        time = parse_datetime(force_text(urlsafe_base64_decode(time)))
        current_time = datetime.datetime.now()
        minutes = (current_time - time).total_seconds() / 60.0
        if minutes > 30:
            return Response({"message": "Reset Link Expired."
            },status=status.HTTP_400_BAD_REQUEST)
        user.set_password(request.data['password'])
        user.save()
        return Response({"message": "Password reset successfull."
        },status=status.HTTP_200_OK)

# ----------------------------------------Re-Set Password----------------------------------------------------
class ResetPasswordView(APIView):
    """
    Reset Password 
    """

    def post(self, request):
        params = request.data
        try:
            user = MyUser.objects.get(email=params['email'])
            if params['password'] == params['confirm-password']:
                if user.check_password(params['password']):
                    return Response({"message": "Password Can't be same as Old Password."
                    },status=status.HTTP_400_BAD_REQUEST)
                else:
                    user.set_password = params['password']
                    user.save()
                    return Response({"message": "Password Change Successfully."
                    }, status=status.HTTP_200_OK)
            return Response({"message": "Password Mismatch."
            }, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"message": "Email Not Regisetered."
            }, status=status.HTTP_400_BAD_REQUEST)

# --------------------------------Profile-Image-Upload-------------------------------------------------------
class UploadProfileImageView(APIView):
    """
    Upload Profile Image 
    """

    def post(self, request):
        params = request.data
        if 'image' in params:
            instance = MyUser.objects.get(email=params['email'])
            image = upload(params['image'])
            instance.image = image['url']
            instance.save()
            return Response({'url': instance.image
            }, status=status.HTTP_200_OK)
        return Response({'message': "image not found "
        }, status=status.HTTP_400_BAD_REQUEST)
#---------------------------------------------------------------------------------------------
class UploadArtistImage(APIView):
    """
    Upload Artist Image
    """
    def post(self,request):
        params = request.data
        print("PARAMS",params)
        try:
            if 'email' in params:
                if 'profile_image' in params and 'work_image' in params:
                    instance = MyUser.objects.get(email=params['email'])
                    profileImage = upload(params['profile_image'])
                    instance.image = profileImage['url']
                    instance.save()
                    artistInstance = Artist.objects.get(user__email=params['email'])
                    workImage = upload(params['work_image'])
                    artistInstance.work_image = workImage['url']
                    artistInstance.save()
                    return Response({'message':"Profile Image Uploaded successfully",'profile': instance.image,"work":artistInstance.work_image
                    }, status=status.HTTP_200_OK)
                return Response({'message':"Image Not Found"
                },status=status.HTTP_400_BAD_REQUEST)
            return Response({"messsage":"Email not in Request"}
            ,status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            print("Exception:",e)
            return Response(status=status.HTTP_400_BAD_REQUEST)

# ---------------------------------------Blog-------------------------------------------------------
# class BlogView(APIView):
#     permission_classes = [IsArtistUser]
#     def get(self, request):
#         blogInstance = Blog.objects.all()
#         serializer = BlogSerializer(blogInstance, many=True)
#         return Response(serializer.data, status=status.HTTP_200_OK)
# ---------------------------------------Get-All-Artist-HomePage-------------------------------------------------------
class GetAllArtistView(APIView):
    """Get all Artis Api"""
    permission_classes = [IsAllUser,]

    def get(self,request):
        serializer=ArtistUserserializer(MyUser.objects.filter(user_type='Artist'),many=True)
        return Response(serializer.data,status=status.HTTP_200_OK)

class GetParticularArtistView(APIView):
    """Get Single Artist information"""
    permission_classes = [IsAllUser, ] 
    def get(self,request):
        try:
            artist_user=MyUser.objects.get(uuid=request.GET['uuid'],user_type='Artist')
            serializer=ArtistUserserializer(artist_user)

            following=Follow.objects.filter(user=artist_user).count()
            followers=Follow.objects.filter(to_follower=artist_user).count()
            photos=Photos.objects.filter(user=artist_user).count()
            return Response({"data":serializer.data,"following":following,"followers":followers,"photos":photos,
            },status=status.HTTP_200_OK)
        except Exception as e:
            print("Exception",e)
            return Response({"message":"you are not access right user_type"
        },status=status.HTTP_404_NOT_FOUND) 

# ---------------------------------------Get-All-Professional-HomePage-------------------------------------------------------
class GetAllProfessionalView(APIView):
    """Get All Professional"""
    permission_classes = [IsAllUser, ]
    def get(self,request):
        serializer=ProfessionalUserserializer(MyUser.objects.filter(user_type='Professional'),many=True)
        return Response(serializer.data,status=status.HTTP_200_OK)

class GetParticularProfessionalView (APIView):
    """Get Single Professional information"""
    permission_classes = [IsAllUser,]
    def get(self,request):
        try:
            professional_user=MyUser.objects.get(uuid=request.GET['uuid'],user_type='Professional')
            serializer=ProfessionalUserserializer(professional_user)
            following=Follow.objects.filter(user=professional_user).count()
            followers=Follow.objects.filter(to_follower=professional_user).count()
            return Response({"data":serializer.data,"following":following,"followers":followers
            },status=status.HTTP_200_OK)
        except Exception as e:
            print("exception",e)
            return Response({"message":"you are not access right user_type"
            },status=status.HTTP_404_NOT_FOUND)
# ---------------------------------------Get-All-Institutional-HomePage-------------------------------------------------------

class GetAllInstitutionalView(APIView):
    """Get All Institution"""
    permission_classes = [IsAllUser,]
    def get(self,request):
        serializer=InstitutionalTypeserializer(MyUser.objects.filter(user_type='Institution'),many=True)
        return Response(serializer.data,status=status.HTTP_200_OK)

class GetParticularInstitutionalView(APIView):
    """Get All Particular Institution information"""
    permission_classes = [IsAllUser,]
    def get(self,request):
        try:
            institution_user=MyUser.objects.get(uuid=request.GET['uuid'],user_type='Institution')
            serializer=InstitutionalTypeserializer(institution_user)

            following=Follow.objects.filter(user=institution_user).count()
            followers=Follow.objects.filter(to_follower=institution_user).count()

            return Response({"data":serializer.data,"following":following,"followers":followers
            },status=status.HTTP_200_OK)
        except Exception as e:
            print("Exception",e)
            return Response({"message":"you are not access right user_type"}
            ,status=status.HTTP_404_NOT_FOUND)

#-----------------------------Follow-User-View----------------------------------------------------------------------------
# class FollowUserView(APIView):
#     """
#     Follow User 
#     """
#     permission_classes = [IsAllUser, ]
#     def get(self, request):
#         try:
#             print(request.user)
#             follow=MyUser.objects.get(uuid=request.GET['uuid'])
#             if follow.uuid != request.user.uuid:
#                 follow,created = Follow.objects.get_or_create(user =request.user,to_follower=follow)
#                 if created:
#                     msg="User followed successfull"
#                 else:
#                     if follow.is_follow:
#                         follow.is_follow = False
#                         msg="User unfollowed successfull"
#                     else:
#                         follow.is_follow = True
#                         msg = "User followed successfull"
#                     follow.save()
#                 return Response({"mesage":msg},status=status.HTTP_200_OK)
#             return Response({'message':"User Can't Follow It self"
#             },status=status.HTTP_400_BAD_REQUEST)
#         except Exception as e:
#             print("Exception",e)
#             print(status=status.HTTP_400_BAD_REQUEST)

#-----------------------------Connect-User-View----------------------------------------------------------------------------

# class ConnectUserView(APIView):
#     """
#     Connect User 
#     """
#     permission_classes=[IsAllUser,]
#     def get(self, request):
#         try:
#             connect = MyUser.objects.get(uuid=request.GET['uuid'])
#             if request.user.uuid != connect.uuid:
#                 connect,created = Connect.objects.get_or_create(user = request.user,connect=connect)
#                 if created:
#                     msg="User connect successfull"
#                 else:
#                     if connect.is_connect:
#                         connect.is_connect = False
#                         msg="User connect unsuccessfull"
#                     else:
#                         connect.is_connect = True
#                         msg = "User connect successfull"
#                     connect.save()
#                 return Response({"mesage":msg},status=status.HTTP_200_OK)
#             return Response({"mesage":"User could'nt be connected by yourself "
#             },status=status.HTTP_400_BAD_REQUEST)
#         except Exception as e:
#             print("Exception",e)
#             return Response(status=status.HTTP_400_BAD_REQUEST)

#-----------------------------Upload-Photos-View----------------------------------------------------------------------------

class UploadArtistPhotosView(APIView):
    """
    Upload Artist Photos
    """
    permission_classes=[IsAllUser,]
    def post(self,request):
        params=request.data
        if 'image' in params:
            photoInstance=Photos.objects.create(user=request.user,title=params['title'])
            image = upload(params['image'])
            photoInstance.image = image['url']
            photoInstance.save()
            return Response({'url': photoInstance.image,
            "title":photoInstance.title
            }, status=status.HTTP_200_OK)
        return Response({'message': "image not found "
        }, status=status.HTTP_400_BAD_REQUEST)

#-----------------------------Gallery-Photos-View----------------------------------------------------------------------------
class UploadArtistGalleryView(APIView):
    permission_classes=[IsAllUser,]
    def post(self,request):
        params=request.data
        if 'image' in params:
            photoInstance=Gallery.objects.create(user=request.user,title=params['title'])
            image = upload(params['image'])
            photoInstance.image = image['url']
            photoInstance.save()
            return Response({'url': photoInstance.image,
            "title":photoInstance.title
            }, status=status.HTTP_200_OK)
        return Response({'message': "image not found "
        }, status=status.HTTP_400_BAD_REQUEST)

#----------------------Project View---------------------------------------------------------------------------------
class ProjectView(APIView):
    permission_classes=[IsInstitutionUser,]
    def post(self,request):
        params=request.data
        print(params)
        try:
            image = upload(params['image'])
            Project.objects.create(
                user=request.user,
                image = image['url'],
                title=params['title'],
                amount=params['amount'],
                description=params['description'],
                rules=params['rules'],
            )
            return Response({"message":"Post created successfully","url":image['url']
            },status=status.HTTP_200_OK)
        except Exception as e:
            print("exception",e)
            return Response({"message":"Image not found"
            },status=status.HTTP_400_BAD_REQUEST)

#--------------------------Bio View---------------------------------------------------------------------------------
class BioView(APIView):
    """
    Add Bio User
    """
    permission_classes=[IsArtistUser,]
    def post(self,request):
        params=request.data
        print("params",params)
        try:
            Bio.objects.create(
                user=request.user,
                bio=params['bio'],
                )
            return Response({"message":"Bio created successfully"
            },status=status.HTTP_200_OK)
        except Exception as e:
            print("exception",e)
            return Response({"message":"Something Went Wrong"
            },status=status.HTTP_404_NOT_FOUND)
            

#------------------------Rating View-------------------------------------------------------------------------------

class RatingView(APIView):
    """
    Rating Of User
    """
    permission_classes=[IsAllUser,]
    def post(self,request):
        params=request.data
        print("params",params)
        try:
            rate=MyUser.objects.get(uuid=params['uuid'])
            ratingInstance, created = Rating.objects.update_or_create(user=request.user,to_rate=rate)
            if created:
                ratingInstance.rating=params['rating']   
            else:
                ratingInstance.rating=params['rating']
            ratingInstance.save()
            return Response({"message":"rating done successfully"
            },status=status.HTTP_200_OK)
        except Exception as e:
            print("exception",e)
            return Response({"message":"something went wrong"
            },status=status.HTTP_400_BAD_REQUEST)


class CalculateRatingView(APIView):
    """
    Calculate Rating of User
    """
    permission_classes=[IsAllUser,]
    def get(self,request):
        try:
            calculate = MyUser.objects.get(uuid=request.GET['uuid'])
            totalInstance = Rating.objects.filter(to_rate=calculate)
            no_of_rate = Rating.objects.filter(to_rate=calculate).count()
            total=0
            for items in totalInstance:
                total+=items.rating
            avg=round((total/no_of_rate),1)
            return Response({"Rating":avg},status=status.HTTP_200_OK)
        except Exception as e:
            print("except",e)
            return Response({"Rating":0,"message":"Rating is not Done"
            },status=status.HTTP_400_BAD_REQUEST)

       
#--------------------------ARTIST-PROFILE-SETUP-------------------------------------------------

class ArtistAndProfessionalBioMediaView(APIView):
    permission_classes=[IsAllUser,]
    def post(self,request):
        print("request",request.user)
        params=request.data
        try:
            bioInstance,created=BiographyLink.objects.get_or_create(user=request.user)
            if 'link' in params:
                bioInstance.image=params['link']
            else:
                image = upload(params['video'],resource_type = "video")
                bioInstance.image=image['url']
            bioInstance.save()
            return Response({"url":bioInstance.image
            },status=status.HTTP_200_OK)
        except Exception as e:   
            print("Exception",e) 
            return Response(status=status.HTTP_400_BAD_REQUEST)


class ArtistAndProfessionalBioView(APIView):
    permission_classes=[IsAllUser,]
    def post(self,request):
        params=request.data
        params['user'] = request.user.id
        try:
            serializer=ArtistAndProfessionalBioSerializer(data=params,context={'params':params})
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data,status=status.HTTP_200_OK)
        except Exception as e:
            print("Exception",e)
            return Response({"message":"something went wrong"},status=status.HTTP_400_BAD_REQUEST)

class ArtistInterestSkillView(APIView):
    """
    Artist Interest and Skill
    """
    permission_classes=[IsArtistUser,]
    def post(self,request):
        params=request.data
        if 'interest' in params:
            for id in params['interest']:
                intrest=UserInterest.objects.get(id=id)
                ArtistUserInterest.objects.get_or_create(user=request.user,user_interest=intrest)
        if 'skill' in params:
            for id in params['skill']:
                skill=UserSkill.objects.get(id=id)
                print("SKILL",skill)
                ArtistUserSkill.objects.get_or_create(user=request.user,user_skill=skill)
        return Response({"msg":"data added successfully"
        },status=status.HTTP_200_OK)

class ArtistAchievementView(APIView):
    """
    Artist Achievement 
    """
    permission_classes=[IsArtistUser,]
    def post(self,request):
        params=request.data
        for key,value in params.items():
            instanace,created =ArtistAchievement.objects.get_or_create(user=request.user,achievement=key)
            if created:
                instanace.no=value
            else:
                instanace.no=value
            instanace.save()
        return Response({"msg":"Achievement Added Successfully"},status=status.HTTP_200_OK)
        
class ArtistExhibitionsView(APIView):
    """
    Artist Exhibitions
    """
    permission_classes=[IsArtistUser,]
    def post(self,request):
        params=request.data
        for key,value in params.items():
            instanace,created =ArtistExhibitions.objects.get_or_create(user=request.user,exhibitions=key)
            if created:
                instanace.no=value
            else:
                instanace.no=value
            instanace.save()
        return Response({"msg":"Exhibitions Added Successfully"
        },status=status.HTTP_200_OK)

class AllUserMediaView(APIView):
    permission_classes=[IsAllUser,]
    def post(self,request):
        params=request.data
        params['user'] = request.user.id

        try:
            serializer=AllUserMediaSerializer(data=params,context={'params':params})
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data,status=status.HTTP_200_OK)
        except Exception as e:
            print("Excption",e)
            return Response(status=status.HTTP_400_BAD_REQUEST)
        
#----------------------------Add Service---------------------------------------
class Service(APIView):
    """
    Add services of users
    """
    permission_classes =[IsAllUser,]
    def post(self,request):
        params=request.data
        print("params",params)
        try:
            for data in params['service']:
                serviceInstance=UserService.objects.get(id=data)
                instance,created = AddUserService.objects.get_or_create(
                    user=request.user,
                    service=serviceInstance
                )
            return Response({"message":"Service Created Successfully"
            },status=status.HTTP_200_OK)
        except Exception as e:
            print("exception",e)
            return Response({"message":"Service does'nt Exsist"},status=status.HTTP_400_BAD_REQUEST)
           
#----------------------------------Add Artist--------------------------------------------
class AddArtist(APIView):
    """
    Add Artist of User
    """
    permission_classes =[IsAllUser,]
    def post(self,request):
        params=request.data
        print("params",params)
        try:
            for data in params['uuid']:
                artistInstance=MyUser.objects.get(uuid=data)
                instance,created = ArtistAdd.objects.get_or_create(
                    user=request.user,
                    artist=artistInstance
                    )  
            return Response({"message":"Artist Created Successfully"
            },status=status.HTTP_200_OK)
        except Exception as e:
            print("exception",e)
            return Response({"message":"Artist does'nt Exsist"},status=status.HTTP_400_BAD_REQUEST)

#-----------------------------------Add Place----------------------------------------------
class AddPlace(APIView):
    """
    Add multiple place of User
    """
    permission_classes =[IsAllUser,]
    def post(self,request):
        params=request.data
        print("params",params)
        try:
            for data in params['place']:
                instance,created = Place.objects.get_or_create(
                    user=request.user,
                    place=data
                    )
            return Response({"message":"Place Created Successfully"
            },status=status.HTTP_200_OK)
        except Exception as e:
            print("exception",e)
            return Response({"message":"Place does'nt Exsist"},status=status.HTTP_400_BAD_REQUEST)

#--------------------------------Team Add--------------------------------------------------------------
class TeamAdd(APIView):
    """
    Add Artist of User
    """
    permission_classes =[IsAllUser,]
    def post(self,request):
        try:
            for data in request.data['uuid']:
                teamInstance=MyUser.objects.get(uuid=data)
                print(teamInstance)
                instance,created = AddTeam.objects.get_or_create(
                    user=request.user,
                    team=teamInstance
                    )  
            return Response({"message":"Team Created Successfully"
            },status=status.HTTP_200_OK)
        except Exception as e:
            print("exception",e)
            return Response({"message":"Team does'nt Exsist"},status=status.HTTP_400_BAD_REQUEST)

#----------------------------------Add Sale----------------------------------------------------------
class AddSale(APIView):
    """
    Add Sale of User
    """
    permission_classes =[IsAllUser,]
    def post(self,request):
        params=request.data
        print("params",params)
        try:
            for data in params['sales']:
                instance,created = ArtistSales.objects.get_or_create(
                    user=request.user,
                    sales=data
                    )
            return Response({"message":"Sales Successfully Created"},status=status.HTTP_200_OK)
        except Exception as e:
            print("exception",e)
            return Response({"message":"Sales does'nt Exsist"},status=status.HTTP_400_BAD_REQUEST)


class AddProject(APIView):
    """
    Add Projects for User
    """
    permission_classes =[IsAllUser,]
    def post(self,request):
        params=request.data
        for key,value in params.items():
            instance,created = UserProject.objects.get_or_create(user=request.user,project=key)
            if created:
                instance.no=value
            else:
                instance.no=value
            instance.save()
        return Response({"message":"Project Added Successfully"
        },status=status.HTTP_200_OK)

#------------------------------Add client-------------------------------------------------------
class AddClientDetails(APIView):
    permission_classes =[IsAllUser,]
    def post(self,request):
        params=request.data
        print("params",params)
        try:
            for data in params['client']:
                instance,created = AddClient.objects.get_or_create(
                    user=request.user,
                    client=data
            )
            return Response({"message":"Client Created Successfully "
            },status=status.HTTP_200_OK)
        except Exception as e:
            print("exception",e)
            return Response({"message":"Client does'nt Exsist"
            },status=status.HTTP_400_BAD_REQUEST)        

class UserAddWork(APIView):
    permission_classes=[IsAllUser,]
    def post(self,request):
        params=request.data
        params['user'] = request.user.id
        try:
            serializer=UserAddWorkSerializer(data=params,context={'params':params})
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data,status=status.HTTP_200_OK)
        except Exception as e:
            print("Excption",e)
            return Response(status=status.HTTP_400_BAD_REQUEST)

class UserAddProject(APIView):
    permission_classes=[IsAllUser,]
    def post(self,request):
        params=request.data
        params['user'] = request.user.id
        try:
            serializer=UserAddProjectSerializer(data=params,context={'params':params})
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data,status=status.HTTP_200_OK)
        except Exception as e:
            print("Excption",e)
            return Response(status=status.HTTP_400_BAD_REQUEST)

class InstitutionInfoServiceActivities(APIView):
    permission_classes=[IsAllUser,]
    def post(self,request):
        params=request.data
        params['user'] = request.user.id
        try:
            serializer=InstitutionInfoServiceSerializer(data=params,context={'params':params})
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data,status=status.HTTP_200_OK)
        except Exception as e:
            print("Excption",e)
            return Response(status=status.HTTP_400_BAD_REQUEST)

#------------------------Artist Get Profile View-----------------------------------------

class ArtistGetProfileViewById(APIView):
    permission_classes=[IsAllUser,]
    def get(self,request):
        try:
            instance=MyUser.objects.get(uuid=request.user.uuid)
            serializer = ArtistGetProfileByIdSerializer(instance)
            following=Follow.objects.filter(user=instance).count()
            ratecount = Rating.objects.filter(to_rate=instance).count()
            followers=Follow.objects.filter(to_follower=instance).count()
            totalInstance = Rating.objects.filter(to_rate=instance)
            total_rating = totalInstance.aggregate(Sum('rating'))['rating__sum']
            try:
                rating=round((total_rating/ratecount),1)
                return Response({"data":serializer.data,'followers':followers,'following':following,"rating":rating,
                },status=status.HTTP_200_OK)
            except:
                return Response({"data":serializer.data,'followers':followers,'following':following,"rating":0,
                },status=status.HTTP_200_OK)
        except Exception as e:
            print("excption",e)
            return Response({"message":"Something went wrong"},status=status.HTTP_400_BAD_REQUEST)
        
class ArtistGetProfileViewByExperience(APIView):
    permission_classes=[IsAllUser,]
    def get(self,request):
        try:
            instance=MyUser.objects.get(uuid=request.user.uuid)
            serializer = ArtistGetProfileByExperienceSerializer(instance)
            following=Follow.objects.filter(user=instance).count()
            ratecount = Rating.objects.filter(to_rate=instance).count()
            followers=Follow.objects.filter(to_follower=instance).count()
            totalInstance = Rating.objects.filter(to_rate=instance)
            total_rating = totalInstance.aggregate(Sum('rating'))['rating__sum']
            try:
                rating=round((total_rating/ratecount),1)
                return Response({"data":serializer.data,'followers':followers,'following':following,"rating":rating,
                },status=status.HTTP_200_OK)
            except:
                return Response({"data":serializer.data,'followers':followers,'following':following,"rating":0,
                },status=status.HTTP_200_OK)
        except Exception as e:
            print("excption",e)
            return Response({"message":"Something went wrong"},status=status.HTTP_400_BAD_REQUEST)
    
class ArtistGetProfileViewByWork(APIView):
    permission_classes=[IsAllUser,]
    def get(self,request):
        try:
            instance=MyUser.objects.get(uuid=request.user.uuid)
            serializer = ArtistGetProfileByWorkSerializer(instance)
            following=Follow.objects.filter(user=instance).count()
            ratecount = Rating.objects.filter(to_rate=instance).count()
            followers=Follow.objects.filter(to_follower=instance).count()
            totalInstance = Rating.objects.filter(to_rate=instance)
            total_rating = totalInstance.aggregate(Sum('rating'))['rating__sum']
            try:
                rating=round((total_rating/ratecount),1)
                return Response({"data":serializer.data,'followers':followers,'following':following,"rating":rating,
                },status=status.HTTP_200_OK)
            except:
                return Response({"data":serializer.data,'followers':followers,'following':following,"rating":0,
                },status=status.HTTP_200_OK)
        except Exception as e:
            print("excption",e)
            return Response({"message":"Something went wrong"},status=status.HTTP_400_BAD_REQUEST)

#--------------------------------------- Professional Get Profile View----------------------------------------

class ProfessionalGetProfileViewById(APIView):
    permission_classes=[IsAllUser,]
    def get(self,request):
        try:
            instance=MyUser.objects.get(uuid=request.user.uuid)
            serializer = ProfessionalGetProfileByIdSerializer(instance)
            following=Follow.objects.filter(user=instance).count()
            ratecount = Rating.objects.filter(to_rate=instance).count()
            followers=Follow.objects.filter(to_follower=instance).count()
            totalInstance = Rating.objects.filter(to_rate=instance)
            total_rating = totalInstance.aggregate(Sum('rating'))['rating__sum']
            try:
                rating=round((total_rating/ratecount),1)
                return Response({"data":serializer.data,'followers':followers,'following':following,"rating":rating,
                },status=status.HTTP_200_OK)
            except:
                return Response({"data":serializer.data,'followers':followers,'following':following,"rating":0,
                },status=status.HTTP_200_OK)
        except Exception as e:
            print("excption",e)
            return Response({"message":"Something went wrong"},status=status.HTTP_400_BAD_REQUEST)


class ProfessionalGetProfileViewByExperience(APIView):
    permission_classes=[IsAllUser,]
    def get(self,request):
        try:
            instance=MyUser.objects.get(uuid=request.user.uuid)
            serializer = ProfessionalGetProfileByExperienceSerializer(instance)
            following=Follow.objects.filter(user=instance).count()
            ratecount = Rating.objects.filter(to_rate=instance).count()
            followers=Follow.objects.filter(to_follower=instance).count()
            totalInstance = Rating.objects.filter(to_rate=instance)
            total_rating = totalInstance.aggregate(Sum('rating'))['rating__sum']
            try:
                rating=round((total_rating/ratecount),1)
                return Response({"data":serializer.data,'followers':followers,'following':following,"rating":rating,
                },status=status.HTTP_200_OK)
            except:
                return Response({"data":serializer.data,'followers':followers,'following':following,"rating":0,
                },status=status.HTTP_200_OK)
        except Exception as e:
            print("excption",e)
            return Response({"message":"Something went wrong"},status=status.HTTP_400_BAD_REQUEST)

class ProfessionalGetProfileViewByWork(APIView):
    permission_classes=[IsAllUser,]
    def get(self,request):
        try:
            instance=MyUser.objects.get(uuid=request.user.uuid)
            serializer = ProfessionalGetProfileByWorkSerializer(instance)
            following=Follow.objects.filter(user=instance).count()
            ratecount = Rating.objects.filter(to_rate=instance).count()
            followers=Follow.objects.filter(to_follower=instance).count()
            totalInstance = Rating.objects.filter(to_rate=instance)
            total_rating = totalInstance.aggregate(Sum('rating'))['rating__sum']
            try:
                rating=round((total_rating/ratecount),1)
                return Response({"data":serializer.data,'followers':followers,'following':following,"rating":rating,
                },status=status.HTTP_200_OK)
            except:
                return Response({"data":serializer.data,'followers':followers,'following':following,"rating":0,
                },status=status.HTTP_200_OK)
        except Exception as e:
            print("excption",e)
            return Response({"message":"Something went wrong"},status=status.HTTP_400_BAD_REQUEST)

#-------------------------------------Institution Get Profile View-----------------------------------
class InstitutionGetProfileViewById(APIView):
    permission_classes=[IsAllUser,]
    def get(self,request):
        try:
            instance=MyUser.objects.get(uuid=request.user.uuid)
            serializer = InstitutionGetProfileByIdSerializer(instance)
            following=Follow.objects.filter(user=instance).count()
            ratecount = Rating.objects.filter(to_rate=instance).count()
            followers=Follow.objects.filter(to_follower=instance).count()
            totalInstance = Rating.objects.filter(to_rate=instance)
            total_rating = totalInstance.aggregate(Sum('rating'))['rating__sum']
            try:
                rating=round((total_rating/ratecount),1)
                return Response({"data":serializer.data,'followers':followers,'following':following,"rating":rating,
                },status=status.HTTP_200_OK)
            except:
                return Response({"data":serializer.data,'followers':followers,'following':following,"rating":0,
                },status=status.HTTP_200_OK)
        except Exception as e:
            print("excption",e)
            return Response({"message":"Something went wrong"},status=status.HTTP_400_BAD_REQUEST)

class InstitutionGetProfileViewByExperience(APIView):
    permission_classes=[IsAllUser,]
    def get(self,request):
        try:
            instance=MyUser.objects.get(uuid=request.user.uuid)
            serializer = InstitutionGetProfileByExperienceSerializer(instance)
            following=Follow.objects.filter(user=instance).count()
            ratecount = Rating.objects.filter(to_rate=instance).count()
            followers=Follow.objects.filter(to_follower=instance).count()
            totalInstance = Rating.objects.filter(to_rate=instance)
            total_rating = totalInstance.aggregate(Sum('rating'))['rating__sum']
            try:
                rating=round((total_rating/ratecount),1)
                return Response({"data":serializer.data,'followers':followers,'following':following,"rating":rating,
                },status=status.HTTP_200_OK)
            except:
                return Response({"data":serializer.data,'followers':followers,'following':following,"rating":0,
                },status=status.HTTP_200_OK)
        except Exception as e:
            print("excption",e)
            return Response({"message":"Something went wrong"},status=status.HTTP_400_BAD_REQUEST)
            

class ArtistImage(APIView):
    def post(self,request):
        params = request.data
        print("params",params)
        try:
            instance = MyUser.objects.get(email=params['email'])
            serializer = ArtistImageSerializer(instance)
            # print(serializer.data)
            return Response(serializer.data,status=status.HTTP_200_OK)
        except Exception as e:
            print("Exception",e)
            return Response({"message":"Something went wrong"},status=status.HTTP_400_BAD_REQUEST)

class ReviewRating(APIView):
    def post(self,request):
        params = request.data
        print("params",params)
        try:
            rated = MyUser.objects.get(uuid=params['uuid'])
            reviewInstance= ReviewAndRating.objects.create(user=request.user,review=params['review'],rating=params['rating'])
            reviewInstance.save()
            return Response({"message":"Review and Rating done successfully"},status=status.HTTP_200_OK)
        except Exception as e:
            print("exception",e)
            return Response({"message":"Something went wrong"},status=status.HTTP_400_BAD_REQUEST)

        

