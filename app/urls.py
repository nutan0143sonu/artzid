from django.conf.urls import url

from app.views import *


urlpatterns = [
    url(r'^signup$', SignUpView.as_view()),
    url(r'^signin$', LoginView.as_view()),
    url(r'^re-send-otp$', ResendOtpView.as_view()),
    url(r'^otp-verification$', OtpVerifyView.as_view()),
    url(r'^forget-password$', ForgotPasswordView.as_view(), name='forget-password'),
    url(r'^reset-password/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<time>[0-9A-Za-z_\-]+)/$',ResetPasswordGetView.as_view(), name='reset-password-get'),
    url(r'^re-set-password$', ResetPasswordView.as_view()),
    url(r'^upload-profile-work-image$', UploadArtistImage.as_view()),
    url(r'^upload-profile-image$', UploadProfileImageView.as_view()),
    # url(r'^blog$', BlogView.as_view()),
    url(r'^get-all-artist-details$', GetAllArtistView.as_view()),
    url(r'^get-all-professional-details$', GetAllProfessionalView.as_view()),
    url(r'^get-all-institutional-details$', GetAllInstitutionalView.as_view()),
    url(r'^get-particular-institution-details$', GetParticularInstitutionalView.as_view()),
    url(r'^get-particular-professional-details$', GetParticularProfessionalView.as_view()),
    url(r'^get-particular-artist-details$', GetParticularArtistView.as_view()),
    # url(r'^follow-user$', FollowUserView.as_view()),
    # url(r'^connect-user$', ConnectUserView.as_view()),
    url(r'^upload-artist-gallery$', UploadArtistGalleryView.as_view()),
    url(r'^upload-artist-photos$', UploadArtistPhotosView.as_view()),
    url(r'^upload-project$', ProjectView.as_view()),
    # url(r'^bio$', BioView.as_view()),
    url(r'^rate-user$', RatingView.as_view()),
    url(r'^calculate-rate$', CalculateRatingView.as_view()),

    url(r'^artist_professional-bio-media$', ArtistAndProfessionalBioMediaView.as_view()),
    url(r'^artist_professional-bio$', ArtistAndProfessionalBioView.as_view()),
    url(r'^user-service$', Service.as_view()),


    url(r'^artist-interest-skill$', ArtistInterestSkillView.as_view()),
    url(r'^artist-achievement$', ArtistAchievementView.as_view()),
    url(r'^artist-exhibitions$', ArtistExhibitionsView.as_view()),
    url(r'^media-upload$', AllUserMediaView.as_view()),
    
    url(r'^add-artist$', AddArtist.as_view()),
    url(r'^add-place$', AddPlace.as_view()),
    url(r'^add-team$', TeamAdd.as_view()),
    url(r'^add-sales$', AddSale.as_view()),
    url(r'^add-project$', AddProject.as_view()),
    url(r'^user-add-work$', UserAddWork.as_view()),
    url(r'^user-add-project$', UserAddProject.as_view()),


    url(r'^user-info-service-activity$', InstitutionInfoServiceActivities.as_view()),
    url(r'^add-client$', AddClientDetails.as_view()),
    url(r'^artist-get-profile-by-id$', ArtistGetProfileViewById.as_view()),
    url(r'^artist-get-profile-by-experience$', ArtistGetProfileViewByExperience.as_view()),
    url(r'^artist-get-profile-by-work$', ArtistGetProfileViewByWork.as_view()),
    url(r'^professional-get-profile-by-id$', ProfessionalGetProfileViewById.as_view()),
    url(r'^professional-get-profile-by-experience$', ProfessionalGetProfileViewByExperience.as_view()),
    url(r'^professional-get-profile-by-work$', ProfessionalGetProfileViewByWork.as_view()),
    url(r'^institution-get-profile-by-id$', InstitutionGetProfileViewById.as_view()),
    url(r'^institution-get-profile-by-experience$', InstitutionGetProfileViewByExperience.as_view()),
    url(r'^artist-profile$', ArtistImage.as_view()),
    url(r'^user-review-rating$', ReviewRating.as_view()),





]