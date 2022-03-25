from django.urls import path,include
#from .views import  RegisterAPIView, login_attempt,register,otp,login_otp,FileView,R
from django.views.generic import TemplateView
from rest_framework import routers
from myapp import views
from . views import *
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView
)
from django.views.decorators.csrf import csrf_exempt
#from django.conf.urls import url
from rest_framework.routers import DefaultRouter

from django.urls import re_path


urlpatterns = [
    path('',TemplateView.as_view(template_name="index.html")),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/token/verify/', TokenVerifyView.as_view(), name='token_verify'),
    path('doc',views.DocView.as_view()),
    path('doc/<int:id>',views.DocView.as_view()), #it is used for the find the videos with id 
    path('accounts/',include('allauth.urls')),
    path('connect',views.communityAPIView.as_view()), #this is used for connect
    path('connect/<int:id>',views.communityAPIView.as_view()),
    path('section',views.AboutAPIView.as_view()), #this is used for aboutsection
    path('section/<int:id>',views.AboutAPIView.as_view()),
    path('profile',views.profileAPIView.as_view()),
    path('profile/<str:id>',views.profileAPIView.as_view()),
    path('groupskill',views.grouplistAPIView.as_view()),
    path('groupskill/<int:id>',views.grouplistAPIView.as_view()),
    path('grouplist',views.playlistAPIView.as_view()),
    path('grouplist/<int:id>',views.playlistAPIView.as_view()),
    path('grouplist/<int:id>&<int:vid>',views.playlistAPIView.as_view()),
    path('general',views.DetailAPIview.as_view()),
    path('general/<str:videoid>',views.DetailAPIview.as_view()),
    path('thumbnail',views.thumbnailapiview.as_view()),
    path('thumbnail/<str:videoid>',views.thumbnailapiview.as_view()),
    path('workbase',views.WorkApiView.as_view()),
    path('workbase/<int:id>',views.WorkApiView.as_view()),
    path('engine/',views.SearchAPIView.as_view()), #this  search for detail 
    path('searchengine/',views.connectSearchAPIView.as_view()), #in the search path we have to use / (slash) this one for connect 
    path('comment',views.commentApiView.as_view()),
    path('comment/<int:id>',views.commentApiView.as_view()),
    path('report',views.reportApiview.as_view()),
    path('otp',views.sendotp.as_view()),
    path('verify',csrf_exempt(views.verifyotp.as_view())),
    path('like/<int:post_id>', views.LikeView.as_view(),name='like'), #for toggel post like 
    path('videolike/<int:detid>',views.videolikeAPi.as_view(),name='videolike'), #for the toggel videolike
    path('resources',views.addresourcesAPIView.as_view()),
    path('resources/<int:id>',views.addresourcesAPIView.as_view()),
    path('question',views.questionnaireAPIView.as_view()),
    path('question/<int:ques_id>',views.questionnaireAPIView.as_view()),
    path('question_text',views.question1APIView.as_view()),
    path('question_text/<int:id>',views.question1APIView.as_view()),
    path('question_QNA',views.question2APIView.as_view()),
    path('question_QNA/<int:id>',views.question2APIView.as_view()),
    path('question_mcq',views.question3APIView.as_view()),
    path('question_mcq/<int:id>',views.question3APIView.as_view()),
    #url(r'^onorall1231aldbSVXVHX/onorall/(?P<id>\d+)$', views.DetailAPIview.as_view()),
    path('example',views.exampleAPIView.as_view()),
    path('example/<int:id>',views.exampleAPIView.as_view()),
    path('basic_display',views.basic_displayAPiView.as_view()),
    path('basic_display/<int:id>',views.basic_displayAPiView.as_view()),
    path('branding',views.basic_brandingAPIView.as_view()),
    path('branding/<int:id>',views.basic_brandingAPIView.as_view()),
    path('wb/<str:workbasename>',views.exAPIView.as_view()),
    path('file',views.APIView.as_view()),
    path('file/<str:id>/<str:name>',views.APIView.as_view()),
    path('monetize',views.ShareMonetize.as_view()),
    path('monetize/<int:id>',views.ShareMonetize.as_view()),
    path('suport',views.supportAPI.as_view()),
    path('suport/<int:id>',views.supportAPI.as_view()),
    path('search/<str:title>',views.multitablesearch.as_view()),
    #path('follow_unfollow/',views.followUnfollow.as_view()),









     #__________________________________________________________________________________:)
    path('comments/<int:pk>/', views.CommentApiView.as_view() , name='all-comment-api-single'),
    path('comments/', views.CommentApiView.as_view() , name='all-comment-api-view'),
    path('reply/', views.ReplyApiView.as_view() , name='all-reply-api-single'),
    path('reply/<int:pk>/', views.ReplyApiView.as_view() , name='all-reply-api-view'),
    path('likes/<int:pk>/', views.LikeApiView.as_view() , name='all-like-api-view-single'),
    path('likes/', views.LikeApiView.as_view() , name='all-like-api-view'),

    path('search/<str:title>', views.multitablesearch.as_view() , name='search-all-like-api-view'),

    #___________________________REFFERAL API
    path('refferal/<int:pk>/', views.RefferalView.as_view() , name='RefferalView-api-view'),
    path('refferal/', views.RefferalView.as_view() , name='AllRefferalView-api-view'),







    # web sockets
    path('wb' , views.index_wb , name="index_wb" ) , 
    path('play/<room_code>', views.game , name='game'),

   
]