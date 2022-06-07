from email.mime import multipart
from email.utils import formatdate
import json
from multiprocessing.sharedctypes import Value
from pickle import TRUE
import re
from urllib import response
from django.shortcuts import render , get_object_or_404
from django.http import JsonResponse
from django.urls.base import reverse_lazy
from django.views.generic import DetailView ,ListView
from django.urls import reverse
from django.views.generic.edit import DeleteView

from rest_framework import status
from django.shortcuts import HttpResponse
from django.http import Http404
from django import http
from django.views.generic.base import View
from datetime import date, datetime
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
import random
from django.http import HttpResponse
import http.client
from django.conf import settings as conf_settings
from django.contrib.auth import authenticate, login
from django.views.generic import View ,CreateView
from django.http import HttpResponseRedirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import authenticate, login
from rest_framework.permissions import IsAuthenticated
from .serializers import *
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.tokens import RefreshToken #this library is used for jwt authentication
from django.conf import settings
from django.core.mail import send_mail
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import authentication, permissions
from rest_framework.parsers import JSONParser,FormParser,MultiPartParser
from django.db.models import Q
import subprocess
from rest_framework.pagination import LimitOffsetPagination
from .tasks import publish_time_celery_task

#___________________________________________________________________________________________________________________________________________

# #Api for video detailing  
# class DetailAPIview(APIView):
#     parser_class=[JSONParser]
#     #parser_classes = (MultiPartParser, FormParser)
#     serializer=DetailSerializer

#     def get(self,request,videoid=None):
#         if videoid:
#             alldetail=detail.objects.get(videoid=videoid)
#             serializer=DetailGetSerializer(alldetail)
#             return Response({'status':'success','data':serializer.data},status=status.HTTP_200_OK)
#         alldetail=detail.objects.all()
#         if request.GET.get('limit') != None and request.GET.get('offset') != None:
#             results = self.paginate_queryset(alldetail, request, view=self)
#             serializer = DetailGetSerializer( results , many=True )
#             return Response({'status':'success','data':serializer.data},status=status.HTTP_200_OK)
#         serializer=DetailSerializer(alldetail,many=True)
#         return Response({'list_of_detail':serializer.data},status=status.HTTP_200_OK)

#     def post(self,request):
#         serializer=DetailSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data,status=status.HTTP_200_OK)
#         else:
#             return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    
#     def patch(self,request,videoid=None):
#         compress=request.data.get('compress')
#         file=detail.objects.get(videoid=videoid)
#         serializer=DetailSerializer(file,data=request.data,partial=True)
#         if serializer.is_valid():
#             if compress=='False':
#                 compressing_video(videoid)
#             serializer.save()
#             return Response({'status':'success','data':serializer.data},status=status.HTTP_200_OK)
#         else:
#             return Response({'status':"error",'data':serializer.errors})

#     def delete(self,request,id=None):
#         event=get_object_or_404(detail,id=id)   
#         event.delete()
#         return Response({'status':'success','data':'items deleted'}) 
#

class thumbnailapiview(APIView):
    def get(self,request,videoid=None):
        if videoid:
            event=detail.objects.get(videoid=videoid)
            serializer=DetailSerializer(event)
            return Response({'status':'success','data':serializer.data},status=status.HTTP_200_OK)
        event=detail.objects.all()
        serializer=DetailSerializer(event,many=True)
        return Response({'status':'success','data':serializer.data},status=status.HTTP_200_OK)

    def patch(self,request,videoid=None):
        event=detail.objects.get(videoid=videoid)
        serializer=DetailSerializer(event,data=request.data,partial=True)
        if serializer.is_valid():
            Automatic_generated_thumbnail(videoid)
            serializer.save()
            return Response({'status':'success','data':serializer.data})
        else:
            return Response({'status':'fail','error':serializer.errors})
        

#______________________________________________________________________________________________________________________
# Api for the for the doc verification
class DocView(APIView):
  parser_classes = (MultiPartParser, FormParser)#[JSONParser]

  serializer_class=doc_verificationSerializer

  def get(self,request,id=None):
        if id:
            alldoc=doc_verification.objects.get(id=id)
            serializer=doc_verificationSerializer(alldoc)
          
            return Response({'status':'success','data':serializer.data},status=status.HTTP_200_OK)
        
        alldocs=doc_verification.objects.all()
        serializer=doc_verificationSerializer(alldocs,many=True)
        return Response({'list_of_communitypost':serializer.data},status=status.HTTP_200_OK)

  def post(self, request, *args, **kwargs):
    doc_serializer = doc_verificationSerializer(data=request.data)
    if doc_serializer.is_valid():
      doc_serializer.save()
      email=request.data.get('email')
      send_mail(
           'Subject here',
           'congratulation,we have recieved your documents .',
           'amitsofficial1998@gmail.com',
            [email],
           fail_silently=False,)
      
      return Response(doc_serializer.data, status=status.HTTP_201_CREATED)
    else:
      return Response(doc_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

  def delete(self, request,  id=None):
        event = get_object_or_404(connect,id=id)
        event.delete()
        return Response({"status":"success","data":"item deleted"} )   

#________________________________________________________________________________________________________________________

# efficient api for the connect model get ,post,patch ,delete 

class communityAPIView(APIView):

    parser_classes = (MultiPartParser, FormParser)
    serializer_class=connectSerializer
    def get(self,request,id=None):
        if id:
            allpost=connect.objects.get(id=id)
            serializer=connectSerializer(allpost)
            return Response({'status':'success','data':serializer.data},status=status.HTTP_200_OK)
        
        allposts=connect.objects.all().prefetch_related('likes')
        serializer=connectSerializer(allposts,many=True)
        return Response(serializer.data,status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        doc_serializer = connectSerializer(data=request.data)
        if doc_serializer.is_valid():
            doc_serializer.save()
            return Response(doc_serializer.data, status=status.HTTP_201_CREATED)
        return Response(doc_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self,request,id=None):
        post=connect.objects.get(id=id)
        serializer=connectSerializer(post,data=request.data,partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({'status':'success','data':serializer.data})
        return Response({'status':"error",'data':serializer.errors})

    def put(self,request,id=None):
        if id:
            post=connect.objects.get(id=id)
            new_id=request.data.get['likes'][0] #----->0 index because we take only first element of the array 
            obj=sign.objects.get(id=str(new_id))
            if obj in post.likes:
                post.like.remove(new_id)
            else:
                post.like.add(new_id)
            post.save()
            serializer=connect_comment_serializer(post)
            return Response({'status':'success','data':serializer.data},status=status.HTTP_200_OK)
        return Response({'status':'fail'},status=status.HTTP_400_BAD_REQUEST)



    def delete(self, request,  id=None):
        event = get_object_or_404(doc_verification,id=id)
        event.delete()
        return Response({"status":"success","data":"item deleted"} ) 

#____________________________________________________________________________________________________________________

#api for about section
class AboutAPIView(APIView):
    parser_classes = [JSONParser]

    def get(self,request,id=None):
        if id:
            allpost=section.objects.select_related('user_profile').get(id=id)
            serializer=tag(allpost)
            return Response({'status':'success','data':serializer.data},status=status.HTTP_200_OK)
        allposts=section.objects.select_related().all()
        serializer=tag(allposts,many=True)
        return Response(serializer.data,status=status.HTTP_200_OK)

    def post(self,request,*args, **kwargs):
        serializer=tag(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self,request,id=None):
        about=section.objects.get(id=id)
        serializer=tag(about,data=request.data,partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({'status':'success','data':serializer.data})
        return Response({'status':"error",'data':serializer.errors})

    def delete(self, request,  id=None):
        event = get_object_or_404(section,id=id)
        event.delete()
        return Response({"status":"success","data":"item deleted"} ) 

#__________________________________________________________________________________________________________

#api for profile
from rest_framework_simplejwt.tokens import RefreshToken
from django.core.exceptions import MultipleObjectsReturned

class profileAPIView(APIView):
    parser_classes = [JSONParser] #(MultiPartParser, FormParser)

    serializer_class=signserializers
    def get(self,request,id=None):
        if id:
            allprofile=sign.objects.get(id=id)
            serializer=signserializers(allprofile)
            return Response({'status':'success','data':serializer.data},status=status.HTTP_200_OK)
        
        allprofile=sign.objects.all()
        serializer=signserializers(allprofile,many=True)
        return Response({'list_of_profile':serializer.data},status=status.HTTP_200_OK)
       

##this post request is used for the jwt authentication
    def post(self,request):
        interest = request.data.get('interest')
        if interest is not None:
            print('deleted--------------')
            del request.data['interest']
        serializer=signserializers( data = request.data )
        gmail=request.data.get('gmail','not found' ).lower()
        phone=request.data.get('phone','not found')
        profile_phone=sign.objects.filter(phone=phone).exists()
        profile_mail=sign.objects.filter(gmail=gmail).exists()

       
        if profile_mail:
            user=sign.objects.get(gmail=gmail)
            print(request.data)
            return Response({'status':200,'response':'gmail  already exist','userid':user.id,'name':user.name,'gmail':user.gmail,'iscreator':user.iscreator},status=status.HTTP_200_OK)
        elif profile_phone :
            user=sign.objects.get(phone=phone)
            refresh = RefreshToken.for_user(user) #this line important for jwt token
            print(request.data)
            return Response({'status':200,'response':'phone already exists','name':user.name,'gmail':user.gmail,'iscreator':user.iscreator,'userid':user.id,'phone':user.phone,'refresh':str(refresh),'access':str(refresh.access_token)})
        if not serializer.is_valid():
            print(request.data)
            return Response({'status':403,'error':serializer.errors})
        
        
        serializer.save()
        user=sign.objects.get(gmail=serializer.validated_data.get('gmail','not found'))
        
        user.interest = interest
        user.save()

        if phone!='not found':
            user=sign.objects.get(phone=serializer.validated_data.get('phone','not found'))
            serializer=signserializers(user)
            refresh = RefreshToken.for_user(user) #this line important for jwt token
            return Response({'status':200,'payload':serializer.data,'refresh':str(refresh),'access':str(refresh.access_token)})


        serializer=signserializers(user)
        refresh = RefreshToken.for_user(user) #this line important for jwt token
        
        return Response({'status':200,'payload':serializer.data,'refresh':str(refresh),'access':str(refresh.access_token)})

   
    def patch(self,request,id=None):
        post=sign.objects.get(id=id)
        date=request.data.get('date_of_birth')
        if date is not None:
           Date_of_birth=datetime.strptime(date, "%Y-%m-%d").date()
           request.data['date_of_birth'] = Date_of_birth
        serializer=signserializers(post,data=request.data,partial=True)
        
        if serializer.is_valid():
            serializer.save()
            return Response({'status':'success','data':serializer.data})
        return Response({'status':"error",'data':serializer.errors})


    def delete(self, request,  id=None):
        event = get_object_or_404(sign,id=id)
        event.delete()
        return Response({"status":"success","data":"item deleted"} ) 
#____________________________________________________________________________________________________
    

#api for groupskills
class groupskillAPIView(APIView):
    parser_classes=(MultiPartParser, FormParser)
    playlist_serializer=groupserializer

    def get(self,request,id=None):
        if id:
            allplaylist=group.objects.select_related('userid').prefetch_related('lists').get(id=id)
            serializer=groupserializer(allplaylist)
            return Response({'status':'success','serializer':serializer.data},status=status.HTTP_200_OK)

        allplaylist=group.objects.select_related('userid' ).prefetch_related('lists').all()
        serializer=groupserializer(allplaylist,many=True)
        return Response({'status':'success','list_of_playlist':serializer.data,},status=status.HTTP_200_OK)

    def post(self,request):
        playlist_serializer=group_post_serializer(data=request.data)
        if playlist_serializer.is_valid():
            playlist_serializer.save()
            return Response(playlist_serializer.data,status=status.HTTP_200_OK)
        return Response(playlist_serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    
    def patch(self,request,id=None):
        list=group.objects.get(id=id)
        serializer=group_post_serializer(list,data=request.data,partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({'status':'success','data':serializer.data})
        return Response({'status':'error','data':serializer.error})

    def put(self,request,id=None):
        event=group.objects.get(id=id)
        new_data=request.data.get(list)
        data=playlist.object.get(id=new_data)
        if data in new_data.list.all():
            new_data.list.remove(new_data)
        else:
            new_data.list.add(new_data)
        event.save()
        serializer=group_post_serializer(event)
        return Response({'status':'success','data':serializer.data},status=status.HTTP_200_OK)


    def delete(self,request,id=None):
        event=get_object_or_404(group,id=id)
        event.delete()
        return Response({'status':'deleted'})


class playlistAPIView(APIView):
    parser_classes= (MultiPartParser, FormParser)
    def get(self,request,id=None,vid=None):
        if request.GET.get('playlist') is not None:
                obj = playlist.objects.select_related('userid').prefetch_related('files').get(id=int(request.GET.get('playlist')))
                serializer = playlist_videoserializer( obj )
                return Response({'data' : serializer.data })

        if id:
            obj =playlist.objects.select_related('userid').prefetch_related('files').get(id=id)
            serializer=playlist_videoserializer(obj )
            if vid:
                file=detail.objects.get(id=vid)
                fileserializer=DetailSerializer(file)
                return Response({'data':fileserializer.data})
            return Response({'status':'success','serializer':serializer.data},status=status.HTTP_200_OK)

        allplaylist=playlist.objects.select_related('userid').prefetch_related('files').all()
        serializer=playlist_videoserializer(allplaylist,many=True)
        return Response({'status':'success','list_of_playlist':serializer.data,},status=status.HTTP_200_OK)

    def post(self,request):
        serializer=playlist_post_videoserializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'status':'success','data':serializer.data},status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

    def patch(self,request,id=None):
        event=playlist.objects.get(id=id)
        serializer=playlist_post_videoserializer(event,data=request.data,partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({'status':'success','data':serializer.data},status=status.HTTP_200_OK)

    def put(self,request,id=None):
        playlist_data=playlist.objects.get(id=id)
        data=request.data.get('files')
        new_id=detail.objects.get(id=data)
        if new_id in playlist_data.files.all():
            playlist_data.files.remove(new_id)
        else:
            playlist_data.files.add(new_id)
        playlist_data.save()
        serializer=playlist_post_videoserializer(playlist_data)
        return Response({'data':serializer.data})

    def delete(self,request,id=None):
        event=get_object_or_404(playlist,id=id)
        event.delete()
        return Response({'item deleted'})


#_______________________________________________________________________________________________________________________
#workbase api
class WorkApiView(APIView):
    parser_classes=  [JSONParser]
    def get(self,request,id=None):
        if id:
            allinfo=workbaseinfo.objects.select_related('userid').get(id=id)
            serializer=workserializer(allinfo)
            return Response({'status':'success','data':serializer.data},status=status.HTTP_200_OK)
        allbaseinfo=workbaseinfo.objects.all()
        serializer=workserializer(allbaseinfo,many=True)
        return Response({'status':'success','data':serializer.data},status=status.HTTP_200_OK)
  
    def post(self,request):
        serializer=workserializer(data=request.data)
        workbasename=request.data.get('workbasename')
        userid=request.data.get('userid')
        sign_obj=sign.objects.get(id=userid)
        work=workbaseinfo.objects.filter(workbasename=workbasename).exists()
        referral_id = int(sign_obj.signup_refferal_by)
        referral_obj = RefferalLink.objects.get(id = referral_id)
        if work:
            return Response({'status':'workbasename already exist'})
        if serializer.is_valid():
            serializer.save()  
            if referral_obj.is_creator == False :
                referral_obj.is_creator = True                               # third condition of referral will be execute
                referral_obj.save()
            return Response({'status':'success','data':serializer.data},status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

from itertools import chain
from rest_framework import filters
from rest_framework import generics
#_______________________________________________________________
class connectSearchAPIView(generics.ListCreateAPIView):
    search_fields = ['^title','^tags','user__name']
    filter_backends = (filters.SearchFilter,)
    queryset = connect.objects.all()
    serializer_class = connectSerializer


#_________________________________________________________________________________________________________________
#api for report 
class reportApiview(APIView):
    parser=(MultiPartParser,FormParser)
    serializer=reportserializer
    def get(self,request,id=None):
        if id:
            reportinfo=report4.objects.get(id=id)
            serializer_info=reportserializer(reportinfo)
            return Response(serializer_info.data,status=status.HTTP_200_OK)

        report_info=report4.objects.all()
        report_serializer=reportserializer(report_info,many=True)
        return Response(report_serializer.data,status=status.HTTP_200_OK)

    def post(self,request,*args,**kwargs):
        serializer=reportserializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_200_OK)

#phone otp
import ast
conn = http.client.HTTPConnection("2factor.in")
parser=(MultiPartParser,FormParser)

class sendotp(APIView):

    def post(self, request, *args, **kwargs):
        name=request.data.get('name')
        phone_number = request.data.get('phone')
        if phone_number:
            phone = str(phone_number)
            user = sign.objects.filter(phone__iexact = phone)
            if user.exists():
                return Response({'user already exist'})
            conn.request("GET", "https://2factor.in/API/V1/7c1b03c3-7905-11ec-b710-0200cd936042/SMS/+91" + phone + "/AUTOGEN") 
            res = conn.getresponse()
           # print(conf_settings.API_KEY)
            data = res.read()
            print(data)
            print(phone)
            return Response({'status':'success','data':data},status=status.HTTP_200_OK)
        else:
            return Response({
                'status' : False,
                'detail' : 'Phone number is not given in post request'
            })  

from django.views.decorators.csrf import csrf_exempt
class verifyotp(APIView):
    def post(self,request,*args,**kwargs):
        otp=request.data.get('otp')
        session_id=request.data.get('session_id')
        if otp:
            conn.request('GET',"https://2factor.in/API/V1/7c1b03c3-7905-11ec-b710-0200cd936042/SMS/VERIFY/"+session_id+"/"+otp+"")
            res=conn.getresponse()
            data=res.read()
            data=data.decode("utf-8")
            data=ast.literal_eval(data)

            if data['Status']=='Success':
                return Response({'status':'verified'},status=status.HTTP_200_OK)
            else:
                return Response('not verified number ')
            
        else:
            return Response({'not otp available'})

#________________________________________________________________________________________________________________________________
class addresourcesAPIView(APIView):
    parser=(MultiPartParser,FormParser)
    def get(self,request,id=None):
        if id:
            reportinfo=Addresources.objects.select_related('video_id' , 'questionnaire' ).get(id=id)
            serializer_info=addresourceserializer(reportinfo)
            return Response(serializer_info.data,status=status.HTTP_200_OK)
        report_info=Addresources.objects.all().select_related('video_id__user_id' , 'questionnaire__videoid' )
        report_serializer=addresourceserializer(report_info,many=True)
        return Response(report_serializer.data,status=status.HTTP_200_OK)

    def post(self,request,*args,**kwargs):
        serializer=addresources_post_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'status':'success','serializer':serializer.data},status=status.HTTP_200_OK)
        else:
            return Response({'data':serializer.errors},status=status.HTTP_400_BAD_REQUEST)

    def delete(self,request,id=None):
        event=get_object_or_404(Addresources,id=id)
        event.delete()
        return Response({'status':'deleted','data':'item deleted'})

class supporttimelineAPI(APIView):

    def get(self,request,id=None):
        if id:
            support_data=supportTimeline.objects.get(id=id)
            serializer=supportgetTimelineserializer(support_data)
            return Response({'status':'success','data':serializer.data},status=status.HTTP_200_OK)
        support_data=supportTimeline.objects.all()
        serializer=supportgetTimelineserializer(support_data,many=True)
        return Response({'status':'success','data':serializer.data},status=status.HTTP_200_OK)

    def post(self,request,*args,**kwargs):
        support_data=supportTimelineserializer(data=request.data)
        if support_data.is_valid():
            support_data.save()
            return Response({'stauts':'success','data':support_data.data},status=status.HTTP_200_OK)
        else:
            return Response({'status':'success','error':support_data.errors},status=status.HTTP_400_BAD_REQUEST)

#___________________________________________________________________________________________________________________
class questionnaireAPIView(APIView):
    parser=[JSONParser]
    serializer=questionnaireserializer
    def get(self,request,ques_id=None):
        if ques_id:
            info=questionnaires.objects.get(ques_id=ques_id)
            serializer=questionnaireserializer(info)
            return Response(serializer.data,status=status.HTTP_200_OK)
        
        info=questionnaires.objects.all()
        serializer=questionnaireserializer(info,many=True)
        return Response(serializer.data,status=status.HTTP_200_OK)
    
    def post(self,request,*args,**kwargs):
        event=questionnairepostserializer(data=request.data)
        if event.is_valid():
            event.save()
            return Response(event.data,status=status.HTTP_200_OK)
        else:
            return Response({'status':'success','data':event.errors},status=status.HTTP_400_BAD_REQUEST)
    
    def patch(self,request,ques_id=None):
        event=Addresources.objects.get(ques_id=ques_id)
        serializer=addresourceserializer(event,data=request.data,partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({'status':'success','data':serializer.data},status=status.HTTP_200_OK)
        else:
            return Response({'status':'success','data':serializer.errors})
    
    def delete(self,request,id=None):
        event=get_object_or_404(questionnaires,id=id)
        event.delete()
        return Response({'status':'success','data':'item deleted'})

#________________________________________________________________________________________________________________
class question1APIView(APIView):
    parser=(MultiPartParser,FormParser)
   
    def get(self,request,ques1id=None):
        if ques1id:
            info=question.objects.get(id=ques1id)
            serializer=question1serializer(info)
            return Response(serializer.data,status=status.HTTP_200_OK)
        
        info=question.objects.select_related('ques').all()
        serializer=question1serializer(info,many=True)
        return Response(serializer.data,status=status.HTTP_200_OK)

    def post(self,request,*args,**kwargs):
        serializer=question1serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'status':'success','data':serializer.data},status=status.HTTP_200_OK)
        return Response({'status':'fail','data':serializer.errors},status=status.HTTP_400_BAD_REQUEST)
    
    def patch(self,request,id=None):
        event=question.objects.get(ques1id=id)
        serializer=question1serializer(event,data=request.data,partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({'status':'success','data':serializer.data},status=status.HTTP_200_OK)
        return Response({'status':'success','data':serializer.errors})

    def delete(self,rerquest,id=None):
        event=get_object_or_404(question,id=id)
        event.delete()
        return Response({'status':'success','data':'item delete'})

class question2APIView(APIView):
    parser=(MultiPartParser,FormParser)
   
    def get(self,request,id=None):
        if id:
            info=question2.objects.get(id=id)
            serializer=question2serializer(info)
            return Response(serializer.data,status=status.HTTP_200_OK)
        info=question2.objects.select_related('questionnaire').all()
        serializer=question2serializer(info,many=True)
        return Response(serializer.data,status=status.HTTP_200_OK)

    def post(self,request,*args,**kwargs):
        serializer=question2serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'status':'success','data':serializer.data},status=status.HTTP_200_OK)
        return Response({'status':'fail','data':serializer.errors},status=status.HTTP_400_BAD_REQUEST)
    
    def patch(self,request,id=None):
        event=question2.objects.get(id=id)
        serializer=question2serializer(event,data=request.data,partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({'status':'success','data':serializer.data},status=status.HTTP_200_OK)
        return Response({'status':'success','data':serializer.errors})
    
    def delete(self,rerquest,id=None):
        event=get_object_or_404(question2,id=id)
        event.delete()
        return Response({'status':'success','data':'item delete'})


class question3APIView(APIView):
    parser=(MultiPartParser,FormParser)
    serializer=questionnaireserializer
    def get(self,request,id=None):
        if id:
            info=question3.objects.select_related('questionnaire').get(id=id)
            serializer=question3serializer(info)
            return Response(serializer.data,status=status.HTTP_200_OK)  
        info=question3.objects.select_related('questionnaire').all()
        serializer=question3serializer(info,many=True)
        return Response(serializer.data,status=status.HTTP_200_OK)

    def post(self,request,*args,**kwargs):
        serializer=question3serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'status':'success','data':serializer.data},status=status.HTTP_200_OK)
        return Response({'status':'fail','data':serializer.errors},status=status.HTTP_400_BAD_REQUEST)
    
    def patch(self,request,id=None):
        event=question3.objects.get(id=id)
        serializer=question3serializer(event,data=request.data,partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({'status':'success','data':serializer.data},status=status.HTTP_200_OK)
        return Response({'status':'success','data':serializer.errors})
    
    def delete(self,request,id=None):
        event=get_object_or_404(question3,id=id)
        event.delete()
        return Response({'status':'success','data':'item delete'})
#__________________________________________________________________________________________________________________
class exampleAPIView(APIView):
    parser=(MultiPartParser,FormParser) #for testing purpose
    serializer=questionnaireserializer
    def get(self,request,id=None):
        if id:
            info=abc.objects.select_related('contact_id').get(id=id)
            serializer=UserSerializer(info)
            return Response(serializer.data,status=status.HTTP_200_OK)
        info=abc.objects.select_related('contact_id').all()
        serializer=UserSerializer(info,many=True)
        return Response(serializer.data,status=status.HTTP_200_OK)

    def post(self,request,*args,**kwargs):
        serializer=UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'status':'success','data':serializer.data},status=status.HTTP_200_OK)
        return Response({'status':'fail','data':serializer.errors},status=status.HTTP_400_BAD_REQUEST)
    
    def patch(self,request,id=None):
        event=abc.objects.get(id=id)
        serializer=UserSerializer(event,data=request.data,partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({'status':'success','data':serializer.data},status=status.HTTP_200_OK)
        return Response({'status':'success','data':serializer.errors})


#_______________________________________________________________________________________________________________________:)
class basic_displayAPiView(APIView):
    parser=[JSONParser] #(MultiPartParser,FormParser)
    def get(self,request,id=None):
        if id:
            event=basic_display.objects.get(id=id)
            serializer=display_serializer(event)
            return Response({'status':'success','data':serializer.data},status=status.HTTP_200_OK)
        event=basic_display.objects.all()
        serializer=display_serializer(event,many=True)
        return Response({'status':'success','data':serializer.data},status=status.HTTP_200_OK)
    
    def post(self,request):
        serializer=basic_display_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'status':'success','data':serializer.data},status=status.HTTP_200_OK)
        return Response({'status':'fail','data':serializer.errors},status=status.HTTP_400_BAD_REQUEST)
        
    def patch(self,request,id=None):
        event=basic_display.objects.get(id=id)
        serializer=basic_display_serializer(event,data=request.data,partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({'status':'success','data':serializer.data},status=status.HTTP_200_OK)
        return Response({'status':'fail','data':serializer.errors},status=status.HTTP_400_BAD_REQUEST)
            

class basic_brandingAPIView(APIView):
    parser=(MultiPartParser,FormParser)
    def get(self,request,id=None):
        if id:
            event=basic_branding.objects.select_related('userid').get(id=id)
            serializer=basic_branding_serializer(event)
            return Response({'status':'success','data':serializer.data},status=status.HTTP_200_OK)
        event=basic_branding.objects.select_related('userid').all()
        serializer=basic_branding_serializer(event,many=True)
        return Response({'status':'success','data':serializer.data},status=status.HTTP_200_OK)
    
    def post(self,request,*args,**kwargs):
        serializer=basic_branding_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'status':'success','data':serializer.data},status=status.HTTP_200_OK)
        return Response({'status':'fail',"data":serializer.errors},status=status.HTTP_400_BAD_REQUEST)

    def patch(self,request,id=None):
        event=basic_branding.objects.get(id=id)
        serializer=basic_branding_serializer(event,data=request.data,partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({'status':'success','data':serializer.data},status=status.HTTP_200_OK)
        return Response({'status':'fail','data':serializer.errors},status=status.HTTP_400_BAD_REQUEST) 
        
from django.core.exceptions import ObjectDoesNotExist
#_______________________________________________________________________________________________________________________
class exAPIView(APIView):
    parser_classes = [JSONParser]
  
    serializer_class=workserializer
    def get(self,request,workbasename=None):
        if workbasename:
            try:
                allinfo=workbaseinfo.objects.select_related().get(workbasename=workbasename)
            except ObjectDoesNotExist:
                return Response({'status':'fail','data':'data does not exists '},status=status.HTTP_400_BAD_REQUEST)
            serializer=workserializer(allinfo)
            return Response({'status':'success','serializer':serializer.data},status=status.HTTP_200_OK)

        allbaseinfo=workbaseinfo.objects.select_related('userid').all()
        serializer=workserializer(allbaseinfo,many=True)
        return Response({'status':'success','data':serializer.data},status=status.HTTP_200_OK)
#_______________________________________________________________________________________________________________________
def findduration(videoid=None):
    file=detail.objects.get(videoid=videoid)
    filepath=str(file)
    video=r"C:\ONORALL\media\\" + filepath
    metadata = subprocess.check_output(f"ffprobe -i {video} -v quiet -print_format json -show_format -hide_banner".split(" "))
    metadata = json.loads(metadata)
    data=f" {float(metadata['format']['duration'])}"
    converted_data=int(float(data))
    result=converted_data//4
    return result
 
#___________________________________________________________________________________________________________________________

def Automatic_generated_thumbnail(videoid=None):
    file=detail.objects.get(videoid=videoid)
    print(file)
    file_path=str(file)
    print(len(file_path))
    frame=findduration(videoid)
    video=r"C:\ONORALL\media\\" + file_path
    output=r"C:\ONORALL\media\\" + file_path
    command=f'ffmpeg -i "{video}" -vf fps=1/{frame} {output}img%0d.jpg'  
    subprocess.run(command, shell=True,stderr=subprocess.STDOUT)
    return Response({'video_thumbnail':video})
#_______________________________________________________________________________________________________________________
def compressing_video(videoid=None):
    file=detail.objects.get(videoid=videoid)
    filepath=str(file)
    print(filepath)
    video=r"C:\ONORALL\media\\" + filepath
    print(video)
    output = r"C:\ONORALL\media\upload\\" + videoid + '\\'+ videoid +'compress.mp4'
    cmd=f'ffmpeg -i "{video}" -vcodec libx264 -crf 28 "{output}"' #crf is the most important thing (constant rate factor)
    print(cmd)
    subprocess.check_output(cmd, shell=True)
#compressing_video( "e6DsT9OZmPQV")
#_______________________________________________________________________________________________________________________
def watermark_on_video(videoid):
    file=detail.objects.get(videoid=videoid)
    filepath=str(file)
    video=r"C:\ONORALL\media\\" + filepath
    print(video)
    output = r"C:\ONORALL\media\upload\\" + videoid + '\\'+ videoid +'watermark'
    cmd=f'ffmpeg -i {input} -ignore_loop 0 -i youtube-logo.gif -filter_complex overlay=shortest=1 {output}' #youtube-logo.gif ki jgha aap apne image ya gif ki location daal skte ho 
    print(cmd)
    subprocess.check_output(cmd, shell=True)

#_______________________________________________________________________________________________________________________
import ffmpeg_streaming
from ffmpeg_streaming import Formats, Bitrate, Representation, Size
def DASH(id=None): #dynamic adaptive bitrate streaming
    file=detail.objects.get(id=id)
    data=str(file)
    resolution_address=data[5::]
    print(len(resolution_address),file)
    video=r"C:\ONORALL\media\file\\" + resolution_address
    _480p = Representation(Size(854, 480), Bitrate(750 * 1024, 192 * 1024))
    #_720p = Representation(Size(1280, 720), Bitrate(2048 * 1024, 320 * 1024))
    #_1080p = Representation(Size(1920, 1080), Bitrate(4096 * 1024, 320 * 1024))
    a = r"C:\Users\user\Downloads\amit2.mp4"
    output =  r"C:\ONORALL\media\dash.mpd"
    video = ffmpeg_streaming.input(a)
    dash = video.dash(Formats.h264())
    dash.representations( _480p)
    dash.output(output)
#DASH(35)
#_____________________________________________________________________________
#share to monitize api
class ShareMonetize(APIView):
    parser=[JSONParser]
    def get(self,request,id=None):
        if id:
            event=sharemon.objects.get(id=id)
            serializer=monitizeserializer(event)
            return Response({'status':'success','data':serializer.data},status=status.HTTP_200_OK)
        monidetail=sharemon.objects.all()
        serializer=monitizeserializer(monidetail,many=True)
        return Response({'status':'success','data':serializer.data},status=status.HTTP_200_OK)

    def post(self,request):
        serializer=monitizeserializer(data=request.data)
        link='http://%s/CretSkill/accept/amit/'%(
            settings.SITE_HOST,
             ) 
        if serializer.is_valid():
            email=request.data.get('email')
            share_email=sharemon.objects.filter(email=email).exists()
            if share_email:
                return Response({'status':'you have already shared this email'}) 
            send_mail(
                     'congratulation,we have recieved your documents .',
                     link,
                     'amitsofficial1998@gmail.com',
                      [email],
                    fail_silently=False,)
            serializer.save()
            return Response({'data':serializer.data,'response':'you have invited your mates'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)




#________________________________________________________________________________________________________________________________
class supportAPI(APIView):
    def get(self,request,id=None):
        if id:
            #support=Support.objects.select_related( 'user' , 'wbname' ).get(id=id)
            support = Support.objects.select_related( 'user' , 'wbname' ).get(id=id)
            serializer = supportserializers(support)
            return Response({'data':serializer.data,'status':'success'},status=status.HTTP_200_OK)
        #support=Support.objects.select_related( 'user' , 'wbname' ).all()
        support = Support.objects.all()
        serializer = supportserializers(support,many=True)
        return Response({'data':serializer.data},status=status.HTTP_200_OK)

    def post(self,request):
        serializer=supportserializers(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'data':serializer.data},status=status.HTTP_200_OK)
        return Response({'status':'fail','data':serializer.errors},status=status.HTTP_400_BAD_REQUEST)

    def delete(self,request,id=None):
        event=get_object_or_404(Support,id=id)
        event.delete()
        return Response({'item deleted'})







#______________________________________________________________________________________________________________________________________
class connect_comment_Api(APIView,LimitOffsetPagination):
    def get(self,request,id=None):
        if id:
            comment=connect_comment.objects.get(id=id)
            serializers=connect_comment_serializer(comment)
            return Response({'data':serializers.data,'status':'success'},status=status.HTTP_200_OK)
        comment_data=connect_comment.objects.all()
        if request.GET.get('limit') != None and request.GET.get('offset') != None:
            results = self.paginate_queryset(comment_data, request, view=self)
            serializer = connect_comment_serializer( results , many=True )
            return Response({'status':'success','data':serializer.data},status=status.HTTP_200_OK)
        serializer=connect_comment_serializer(comment_data,many=True)
        return  Response({'data':serializer.data,'status':'success'},status=status.HTTP_200_OK)

    def post(self,request,*args,**kwargs):
        serializer=connect_comment_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'data':serializer.data,'status':'success'},status=status.HTTP_200_OK)

    def patch(self,request,id=None):
        comment_data=connect_comment.objects.get(id=id)
        serializer=connect_comment_serializer(comment_data,data=request.data,partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({'status':'success','data':serializer.data},status=status.HTTP_200_OK)

    
class LikeApiView( APIView ):

    def get( self , request , pk = None  , *args , **kwargs ):
        if pk is not None:
            like_obj = get_object_or_404(LikeModel ,  user = pk )
            serializer = LikeModelSerializer( like_obj )
            return Response({'status':'success','data':serializer.data , 'total likes' : like_obj.total_likes},status=status.HTTP_200_OK)
        all_like_obj  = LikeModel.objects.all()
        serializer = LikeModelSerializer( all_like_obj , many=True )
        return Response({'status':'success','data':serializer.data},status=status.HTTP_200_OK)

    def post(self,request, pk = None , *args, **kwargs):
        serializer = LikeModelSerializer( data = request.data )
        if serializer.is_valid():
            serializer.save()
            return Response({'status':'success','data':serializer.data},status=status.HTTP_200_OK)
        return Response({'status':'fail',"data":serializer.errors},status=status.HTTP_400_BAD_REQUEST)

    
    def put(self,request,pk=None):
        if pk:
            user_data=LikeModel.objects.get(user=str(pk))
            new_id=request.data.get('videos') #----->0 index because we take only first element of the array 
            print(new_id,'hhhhh')
            obj=detail.objects.get(id=new_id)
            if obj in user_data.videos.all():
                user_data.videos.remove(new_id)
            else:
                user_data.videos.add(new_id)
            user_data.save()
            serializer=LikeModelSerializer(user_data)
            return Response({'status':'success','data':serializer.data},status=status.HTTP_200_OK)
        return Response({'status':'fail'},status=status.HTTP_400_BAD_REQUEST)



    def delete(self,request,id=None):
        event=get_object_or_404(connect_comment,id=id)
        event.delete()
        return Response({'status':'item deleted successfully'})
#__________________________________________________________________________________________________________________________________________
class videoviewApi(APIView):
     def get(self,request,id=None):
        if id:
            video=view.objects.get(id=id)
            video.view=video.view+1
            video.save()
            serializers=video_view_serializer(video)
            return Response({'data':serializers.data,'status':'success'},status=status.HTTP_200_OK)
#__________________________________________________________________________________________________________________________________________
import socket   
hostname = socket.gethostname()   #>>>>>>this is used to find the ip address
IPAddr = socket.gethostbyname(hostname)   
print("Your Computer Name is:" + hostname)   
print("Your Computer IP Address is:" + IPAddr)  







class questionnaireAPIView(APIView):
    parser=(MultiPartParser,FormParser)
    serializer=questionnaireserializer
    def get(self,request,ques_id=None):
        if ques_id:
            info=questionnaires.objects.get(ques_id=ques_id)
            serializer=questionnaireserializer(info)
            return Response(serializer.data,status=status.HTTP_200_OK)

        context, all_obj = self.custom_efficient_method(request)
        serializer=questionnaireserializer(all_obj,many=True)
        return Response(serializer.data,status=status.HTTP_200_OK)

    def custom_efficient_method(self, request):   
        context = { "request": request }  
        all_objs =  questionnaires.objects.all()
        all_obj = questionnaireserializer.setup_eager_loading(all_objs)
        return context,all_obj    
    
    
    def post(self,request,*args,**kwargs):
        serializer=questionnaireserializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return response({'status':'success','data':serializer.data},status=status.HTTP_200_OK)
        return Response({'status':'success','data':serializer.data},stauts=status.HTTP_200_OK)
    
    def patch(self,request,ques_id=None):
        event=Addresources.objects.get(ques_id=ques_id)
        serializer=addresourceserializer(event,data=request.data,partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({'status':'success','data':serializer.data},status=status.HTTP_200_OK)
        return Response({'status':'success','data':serializer.errors})
    
    def delete(self,request,id=None):
        event=get_object_or_404(questionnaires,id=id)
        event.delete()
        return Response({'status':'success','data':'item deleted'})






























#_________________________________________________________________________________________________________________________________________
# API's for Comments 
class CommentApiView( APIView,LimitOffsetPagination ):

    def get( self , request , pk = None  , *args , **kwargs ):
        if  pk is not None:
            comment_obj = get_object_or_404( Commentss , id = pk )
            serializer = CommentSerializer_single_instance( comment_obj )
            return Response({'status':'success','data':serializer.data},status=status.HTTP_200_OK)
            
        all_comments_obj =  Commentss.objects.all().prefetch_related('likes_on_comment' , 'dis_likes_on_comment')

        if request.GET.get('limit') != None and request.GET.get('offset') != None:
            results = self.paginate_queryset(all_comments_obj, request, view=self)
            serializer = CommentSerializer( results , many=True )
            return Response({'status':'success','data':serializer.data},status=status.HTTP_200_OK)

        context, all_obj = self.custom_efficient_method(request)
        serializer = CommentSerializer( all_obj , many=True )
        return Response(serializer.data,status=status.HTTP_200_OK)

    def custom_efficient_method(self, request):   
        context = { "request": request }  
        all_objs =   Commentss.objects.all().prefetch_related('likes_on_comment' , 'dis_likes_on_comment')
        all_obj = CommentSerializer.setup_eager_loading(all_objs)
        return context,all_obj    
        
        
    

    def post(self,request, pk = None , *args, **kwargs):
        serializer = CommentSerializer( data = request.data )
        if serializer.is_valid():
            serializer.save()
            return Response({'status':'success','data':serializer.data},status=status.HTTP_200_OK)
        return Response({'status':'fail',"data":serializer.errors},status=status.HTTP_400_BAD_REQUEST)


    def patch( self , request, pk = None, *args , **kwargs ):
        if pk is not None:
            queryset =  Commentss.objects.get( id = pk )
            serializer= CommentSerializer( queryset , data=request.data , partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response({'status':'success','data':serializer.data},status=status.HTTP_200_OK)
            return Response({'status':'fail','data':serializer.errors},status=status.HTTP_400_BAD_REQUEST) 
        return Response({'status':'fail','data':'please provide id in url '},status=status.HTTP_400_BAD_REQUEST) 

   
    def put(self, request, pk=None , format=None):
        if pk is not None:
            obj = Commentss.objects.get( id = pk)
            if request.data['action'] == "like" :
                new_ids = request.data.get('likes_on_comment')              
                sign_obj = sign.objects.get(id=str(new_ids[0]))               
                if sign_obj not in obj.likes_on_comment.all() :              
                    obj.likes_on_comment.add(sign_obj)
                    obj.like_active ='liked'
                    obj.save()
                    if sign_obj in obj.dis_likes_on_comment.all():
                        obj.dis_likes_on_comment.remove(sign_obj)
                        obj.dislike_active ='null'
                        obj.save()
                        serializer = CommentSerializer(obj)
                        return Response({'status':'remove-dislike-success','data':serializer.data},status=status.HTTP_200_OK)
                else:
                    obj.likes_on_comment.remove(sign_obj)
                    obj.like_active = 'null'
                    obj.save()
                    serializer = CommentSerializer(obj)
                    return Response({'status':'removelike-success','data':serializer.data},status=status.HTTP_200_OK)
                serializer = CommentSerializer(obj)
                return Response({'status':'removelike-success','data':serializer.data},status=status.HTTP_200_OK)
            else :
                new_ids = request.data.get('dis_likes_on_comment')        
                sign_obj = sign.objects.get(id=str(new_ids[0]))
                if sign_obj in obj.dis_likes_on_comment.all():
                    obj.dis_likes_on_comment.remove(sign_obj)
                    obj.dislike_active = 'null'
                    obj.save()
                    serializer = CommentSerializer(obj)
                    return Response({'status':'remove-dislike-success','data':serializer.data},status=status.HTTP_200_OK)
                else:
                    obj.dis_likes_on_comment.add(sign_obj)
                    obj.dislike_active ='disliked' 
                    obj.save() 
                    if sign_obj in obj.likes_on_comment.all():
                        obj.likes_on_comment.remove(sign_obj)
                        obj.like_active ='null'
                        obj.save()
                        serializer = CommentSerializer(obj)
                        return Response({'status':'removedis-like-success','data':serializer.data},status=status.HTTP_200_OK)
                    serializer = CommentSerializer(obj)
                    return Response({'status':'add-dis-like-success','data':serializer.data},status = status.HTTP_200_OK)


    def delete( self , request , pk= None , *args , **kwargs ):
        if pk is not None:
            queryset =  Commentss.objects.get(id=pk)    
            queryset.delete()
            return Response({'status':'deleted' },status=status.HTTP_200_OK)
        return Response({'status':'fail','data':"DoesNotExist"},status=status.HTTP_400_BAD_REQUEST) 


class CommentApiForVideoView(APIView):
    def get( self , request , pk = None  , *args , **kwargs ):
        if pk is not None:
            myvideoId = detail.objects.get(videoid=pk)
            comment_obj = Commentss.objects.filter(  video_id = myvideoId ) 
            serializer = CommentSerializer( comment_obj , many=True)
            return Response({'status':'success','data':serializer.data},status=status.HTTP_200_OK)
        return Response({'status':'fail provide videoid ',},status=status.HTTP_400_BAD_REQUEST)





from django.db.models import Q
def querys_for_workbase(  title  ):
    title = title.strip().replace('/' , '') 
    query , count  ,  n , temp = str() , 0 ,  len(title) ,  len(title)
    if n > 9 :
        while temp-3 > 0:
            count = 0
            if (n - count) <= 5 :                       # last minimum query = Q(workbasename__icontains = title[:6] 
                break
            query = query + f"Q(workbasename__icontains = title[:{n - count}] ) | "  
            count += 1
            n = n-3                                                        
            temp = temp - 1
        return query 
    return None

def querys_for_detail(  title  ):
    title = title.strip().replace('/' , '')
    query , count  ,  n , temp = str() , 0 ,  len(title) ,  len(title)
    count= 0
    if n > 9 :
        while temp-3 > 0:
            count = 0
            if (n - count) <= 5 :                       # last minimum query = Q(workbasename__icontains = title[:6] 
                break
            query = query + f"Q(title__icontains = title[:{n - count}] ) | "  
            count += 1
            n = n-3
            temp = temp - 1
        return query 
    return None



class multitablesearch(APIView):
    def get( self , request , title = None  , *args , **kwargs ):
        combine_query = {}
        if title is not None:   

            querys_1 = querys_for_detail(title)

            detail_obj =  detail.objects.filter( Q(title__icontains = title ) ).prefetch_related('likesvideo').order_by('published_on') if querys_1  is None else  detail.objects.filter(eval(querys_1[:(len(querys_1)-2)]) ).prefetch_related('likesvideo').order_by('published_on')
            serializer = DetailSerializer( detail_obj  , many=True )
            combine_query[' detail result '] = serializer.data 

            querys_2 = querys_for_workbase(title)
            print(querys_2)
            workbase_obj =  workbaseinfo.objects.filter( Q(workbasename__icontains = title) ).select_related('userid') if querys_2  is None else  workbaseinfo.objects.filter(eval(querys_2[:(len(querys_2)-2)]) ).select_related('userid')
            serializer1 = workserializer( workbase_obj , many = True )
            combine_query[' workbase result '] = serializer1.data
            return Response({'status':'success','data': combine_query },status=status.HTTP_200_OK)
        return Response({'status':'fail','data':"provide query in url" },status=status.HTTP_400_BAD_REQUEST) 


        
        '''
            # = detail.mongo_manager.raw_query( { '$text' : { '$search' :  title } }  ).prefetch_related('likesvideo')
            #detail_obj = detail.mongo_manager.raw_query( { '$text' : { '$search' :  title } } ).raw_query({'score' : {'$meta':'textScore' } }).prefetch_related('likesvideo')

            dense_rank_by_year = Window( expression=DenseRank(), partition_by=F("title"), order_by=F("published_on").desc())
            commiters_with_rank = detail.objects.filter( title__icontains = title ).annotate( the_rank=dense_rank_by_year ).order_by("-published_on", "the_rank")

            if want to rank our result and do advance search features then use POSTgres SearchVector , SearchQuery , trigrame_similarity
        '''
# usr = sign.objects.first()

# det = detail.objects.get(videoid="VmGjxoZIT0zK")
# for i in range(10):
#     print(i)
#     sign.objects.create(gmail = f"faker{i+1}@gmail.com" , name = f'faker_name{i}')
#     if i ==50:
#         print('50>>>>>>>>>>>>>>>>>')

class RefferalView( APIView ):

    def get( self , request , pk = None  , *args , **kwargs ):
        if pk is not None:
            refferal_obj = get_object_or_404(RefferalLink ,  id = pk )
            serializer = RefferalLinkSerializer( refferal_obj )
            return Response({'status':'success','data':serializer.data},status=status.HTTP_200_OK)
        all_like_obj  = RefferalLink.objects.all()
        serializer = RefferalLinkSerializer( all_like_obj , many=True )
        return Response({'status':'success','data':serializer.data},status=status.HTTP_200_OK)

    def post(self,request, pk = None , *args, **kwargs):
        serializer = RefferalLinkSerializer( data = request.data )
        if serializer.is_valid():
            serializer.save()
            return Response({'status':'success','data':serializer.data},status=status.HTTP_200_OK)
        return Response({'status':'fail',"data":serializer.errors},status=status.HTTP_400_BAD_REQUEST)

    def patch(self,request,pk= None, *args , **kwargs ) :
        if pk is not None:
            queryset = get_object_or_404(RefferalLink ,  id = pk )
            serializer= RefferalLinkSerializer( queryset , data=request.data , partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response({'status':'success','data':serializer.data},status=status.HTTP_200_OK)
            return Response({'status':'fail','data':serializer.errors},status=status.HTTP_400_BAD_REQUEST) 
        return Response({'status':'fail','data':'please provide id in url '},status=status.HTTP_400_BAD_REQUEST) 

    def delete( self, request, pk= None, *args , **kwargs ):
        if pk is not None:
            queryset =  RefferalLink.objects.get(id=pk)
            if queryset.exists():
                queryset.delete()
            return Response({'status':'deleted' },status=status.HTTP_200_OK)
        return Response({'status':'fail','data':"DoesNotExist"},status=status.HTTP_400_BAD_REQUEST) 

            

#__________________________________________________________________________________________________________________________
def random_id_field():
  rnd_id = ''.join(random.choices(string.ascii_letters + string.digits, k=12))
  return rnd_id


from django.views.decorators.cache import cache_page
from django.utils.decorators import method_decorator


class DetailAPIview(APIView):
    pareser_class=[JSONParser]
    #parser_classes = (MultiPartParser, FormParser)
    serializer=DetailSerializer

    @method_decorator(cache_page(60 * 2))
    def get(self,request,videoid=None):
        if videoid:
            alldoc=detail.objects.get(videoid=videoid)
            serializer=DetailSerializer(alldoc)
            return Response({'status':'success','data':serializer.data},status=status.HTTP_200_OK)
        
        alldocs=detail.objects.all()
        serializer=DetailSerializer(alldocs,many=True)
        return Response({'list_of_detail':serializer.data},status=status.HTTP_200_OK)

    def post(self,request):
        serializer=DetailSerializer(data=request.data)
        if serializer.is_valid():
            try:
                sign_obj = sign.objects.get(id = str(request.data['userid']))  
            except :
                sign_obj = sign.objects.get(id = str(request.data['userid']['id']))
            sign_ref = sign_obj.signup_refferal_by
            if sign_ref != 0:
                referral_obj = RefferalLink.objects.get(id= int(sign_ref))
                if referral_obj.is_uploaded == False:
                    referral_obj.is_uploaded = True                 # fourth condtion of referralLink will be executed
                    referral_obj.save()
            serializer.save()
            return Response(serializer.data,status=status.HTTP_200_OK)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    
    def patch(self,request,videoid=None):
        compress=request.data.get('compress')
        file=detail.objects.get(videoid=videoid)
        serializer=DetailSerializer(file,data=request.data,partial=True)
        if serializer.is_valid():
            if compress=='False':
                compressing_video(videoid)
            serializer.save()
            return Response({'status':'success','data':serializer.data},status=status.HTTP_200_OK)
        return Response({'status':"error",'data':serializer.errors})

    def put( self , request , videoid=None , format=None ):
        if videoid is not None :
            obj = detail.objects.get( videoid = videoid)                          
            new_ids = request.data['likesvideo'][0]                  # get the userid who want to like    
            sign_obj = sign.objects.get(id=str(new_ids))             # get the like-person from thw userid   
            if sign_obj in obj.likesvideo.all():                     # if like-person already liked
                obj.likesvideo.remove( sign_obj )                    # then remove the like-person in likesvideo
            else:                                                    # else        
                obj.likesvideo.add( sign_obj )                       # add  the like-person in likesvideo  
            obj.save()                                               # save the object        
            serializer = DetailSerializer(obj)                       # simple render the video data
            return Response( { 'status' : 'success','data':serializer.data } , status=status.HTTP_200_OK)
        return Response({'status':'fail','data':' provide  videoid of generaAPI in url '},status=status.HTTP_400_BAD_REQUEST)

    def delete(self,request,id=None):
        event=get_object_or_404(detail,id=id)   
        event.delete()
        return Response({'status':'success','data':'items deleted'}) 

import json
class WorkApiView(APIView):
    parser_classes=  [JSONParser]
    def get(self,request,id=None):
        if id:
            allinfo=workbaseinfo.objects.get(id=id)
            serializer=workserializer(allinfo)
            return Response({'status':'success','data':serializer.data},status=status.HTTP_200_OK)
        allbaseinfo=workbaseinfo.objects.all()
        serializer=workserializer(allbaseinfo,many=True)
        return Response({'status':'success','data':serializer.data},status=status.HTTP_200_OK)
  
    def post(self,request):
        serializer=workserializer(data=request.data)
        workbasename=request.data.get('workbasename')
        work = workbaseinfo.objects.filter(workbasename=workbasename).exists()  
        sign_obj = sign.objects.get(id = request.data['userid'])     
        if work:
            return Response({'status':'workbasename already exist'})
        if serializer.is_valid():   
            sign_obj.iscreator = True                                             #:)''' this is for iscreator true in sign models '''
            sign_obj.save()                                                     
            if sign_obj.signup_refferal_by != 0:
                referral_id = int(sign_obj.signup_refferal_by)
                referral_obj = RefferalLink.objects.get(id = referral_id)
                if referral_obj.is_creator == False :
                    referral_obj.is_creator = True                               # third condition of referral will be execute
                    referral_obj.save()
                serializer.save()
                return Response({'status':'success','data':serializer.data},status=status.HTTP_200_OK)
            else:
                serializer.save()
                return Response({'status':'success','data':serializer.data},status=status.HTTP_200_OK)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

    def patch(self,request,id=None):
        post=workbaseinfo.objects.get(id=id)
        serializer=workserializer(post,data=request.data,partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({'status':'success','data':serializer.data})    
        return Response({'status':"error",'data':serializer.errors})

    def delete(self, request,  id=None):
        event = get_object_or_404(workbaseinfo,id=id)
        event.delete()
        return Response({"status":"success","data":"item deleted"}) 

#_____________________________________________________________________________________________________________________
class profileRefferalAPIView(APIView):
    def get( self , request,code=None):
        if code is not None:
            referral_code = str(code)
            referral_obj = RefferalLink.objects.get(refferal_code = referral_code)
            if referral_obj.is_clicked == False:    
                request.session['referral_code'] = referral_code         # store in session
                referral_obj.is_clicked = True                           # referral step - 1 
                referral_obj.save()
            serializer=RefferalLinkSerializer(referral_obj)
            return Response({'status':'success','data':serializer.data},status=status.HTTP_200_OK)
        all_ref = RefferalLink.objects.all()
        serializer=RefferalLinkSerializer( all_ref ,many=True)
        return Response({'status':'success','data':serializer.data},status=status.HTTP_200_OK)
  

    def post( self , request , code = None , *args , **kwargs ):
        if code is not None :
            referral_code = str(code)
            referral_obj = RefferalLink.objects.get(refferal_code = referral_code)
            serializer=signserializers(data=request.data)
            # before saving the gmail should be in lowercase
            gmail = request.data.get('gmail'  , 'not found').lower()
            phone=request.data.get('phone'  , 'not found')
            profile_phone=sign.objects.filter(phone=phone).exists()
            profile_mail=sign.objects.filter(gmail=gmail).exists()
            if profile_mail:
                user=sign.objects.get(gmail=gmail)
                return Response({'status':200,'response':'gmail already exists','name':user.name,'gmail':user.gmail,'refresh':str(refresh),'access':str(refresh.access_token)})
            elif profile_phone:
                user=sign.objects.get(phone=phone)
                refresh = RefreshToken.for_user(user)                       #this line important for jwt token
                return Response({'status':200,'response':'phone already exists','name':user.name,'gmail':user.gmail,'refresh':str(refresh),'access':str(refresh.access_token)})
            
            if not serializer.is_valid(raise_exception=True):
                return Response({'status':403,'error':serializer.errors})
            serializer.validated_data['signup_refferal_by'] = int(referral_obj.id)
            serializer.save()
            if request.session.has_key('referral_code'):
                if referral_obj.is_signup == False:
                    referral_obj.is_signup = True                         # referral step - 2
                    referral_obj.save()
                    del request.session['referral_code']                  # delete the session value
            if phone:
                user=sign.objects.get(phone=serializer.validated_data.get('phone' , 'not found'))
                refresh = RefreshToken.for_user(user)                     # this line important for jwt token
            user=sign.objects.get(gmail=serializer.validated_data.get('gmail' , 'not found'))
            refresh = RefreshToken.for_user(user)                     # this line important for jwt token
            return Response({'status':200,'payload':serializer.data,'refresh':str(refresh),'access':str(refresh.access_token)})
            



class course_list(APIView):
    parser = (MultiPartParser , FormParser)
    def get(self,request , pk=None ):
        if pk :
            event=mycourse.objects.get(id=pk)
            serializer=courseserializer(event)
            return Response({'data':serializer.data})

        event=mycourse.objects.all()
        serializer=courseserializer(event,many=True)
        return Response({'data':serializer.data})

    def post(self,request , pk=None , *args , **kwargs ):
        serializer=courseserializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'status':serializer.data},status=status.HTTP_200_OK)
        return Response({'status':'fail','error':serializer.errors},status=status.HTTP_400_BAD_REQUEST)


    def patch(self,request , pk=None , *args , **kwargs ):
        obj = mycourse.objects.get(id=pk )
        serializer=courseserializer( obj ,data=request.data,partial=True)
        if serializer.is_valid():
            new_id = int(request.data.get('course_playlist'))
            new_obj_playlist = playlist.objects.filter(id=new_id).exists()
            new_obj_detail = detail.objects.filter(id=new_id).exists()

            if new_obj_playlist:
                if new_obj_playlist not in obj.course_playlist.all():
                    obj.course_playlist.add(new_obj_playlist)
                    serializer.save()
                    return Response({'status' : 'added in playlist '  , 'data':serializer.data , },status=status.HTTP_200_OK)

            elif  new_obj_detail :
                if new_obj_playlist not in obj.course_file.all():
                    obj.course_file.add(new_obj_playlist)
                    serializer.save()
                    return Response({'status' : 'added in detail '  ,  'data':serializer.data},status=status.HTTP_200_OK)

            else:
                serializer.save()
                return Response({'status':"not found Details/playlist"},status=status.HTTP_400_BAD_REQUEST)

            return Response({'status':'success','data':serializer.data})    
        return Response({'status':"error",'data':serializer.errors})




    

#___________________--report api
class reportApiview(APIView):
    parser=(MultiPartParser,FormParser)
    serializer=reportserializer
    def get(self,request,reportid=None):
        if reportid:
            reportinfo=report4.objects.get(id=reportid)
            info = {}
            try:                                                                                               # use try except because one condition always will be false and one true
                count_video = report4.objects.filter( report_file = reportinfo.report_file ).count()            # get the total count of report of this video
                info['total_report_of_this_file'] = count_video
            except :                                                                             
                count_post = report4.objects.filter( report_post = reportinfo.report_post ).count()             # get the total count of report of this video
                info['total_report_of_this_post'] = count_post
            serializer_info=reportserializer(reportinfo)
            return Response({'status' : 'success','data' : serializer_info.data  , 'additional_data' : info} ,status=status.HTTP_200_OK)  
        report_info=report4.objects.all()
        report_serializer=reportserializer(report_info,many=True)
        return Response({'status':'success','data':report_serializer.data} ,status=status.HTTP_200_OK)

    def post(self,request,*args,**kwargs):
        serializer=reportserializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_200_OK)
        return Response({'status':'success','data':serializer.data} ,status=status.HTTP_400_BAD_REQUEST)



class ReplyApiView( APIView ):

    def get( self , request , pk = None  , *args , **kwargs ):
        if pk is not None:
            reply_obj = get_object_or_404(Reply ,  id = pk )
            serializer = ReplySerializer( reply_obj )
            return Response({'status':'success','data':serializer.data},status=status.HTTP_200_OK)
        all_reply_obj  = Reply.objects.all()
        serializer = ReplySerializer( all_reply_obj , many=True )
        return Response({'status':'success','data':serializer.data},status=status.HTTP_200_OK)

    def post(self,request, pk = None , *args, **kwargs):
        serializer = ReplySerializer( data = request.data )
        if serializer.is_valid():
            serializer.save()
            return Response({'status':'success','data':serializer.data},status=status.HTTP_200_OK)
        return Response({'status':'fail',"data":serializer.errors},status=status.HTTP_400_BAD_REQUEST)


    def patch(self,request,pk= None, *args , **kwargs ):
        if pk is not None:
            queryset = get_object_or_404(Reply  , id =pk)
            serializer= ReplySerializer( queryset , data=request.data , partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response({'status':'success','data':serializer.data},status=status.HTTP_200_OK)
            return Response({'status':'fail','data':serializer.errors},status=status.HTTP_400_BAD_REQUEST) 
        return Response({'status':'fail','data':'please provide id in url '},status=status.HTTP_400_BAD_REQUEST) 

    def delete( self, request, pk = None, *args , **kwargs ):
        if pk is not None:
            queryset =  Reply.objects.get( id=pk)
            if queryset.exists():
                queryset.delete()
            return Response({'status':'deleted' },status=status.HTTP_200_OK)
        return Response({'status':'fail','data':"DoesNotExist"},status=status.HTTP_400_BAD_REQUEST) 



class APIView(APIView):
    parser_classes = (MultiPartParser,FormParser)
    def post(self,request,*args,**kwargs):
        name=request.data.get('name')
        gmail=request.data.get('gmail')
       
        try:
            if Contact.objects.filter(name=name).exists():
                return Response({'username is taken'})
            if Contact.objects.filter(gmail=gmail).exists():
                return Response({'Email is taken'})
            auth_token=str(uuid.uuid4())
            print('ddddd',auth_token)
            user_obj=Contact.objects.create(name=name,gmail=gmail,auth_token=auth_token)
            serializer=ContactSerializerModel(user_obj)
            send_mail_registration(gmail,auth_token)
            return Response({'data':serializer.data})
        except Exception as e:
            print(e)

class VerifyEmail(APIView):
    def get(self,request,token=None):
        if token:
           user_obj=Contact.objects.get(auth_token=token)
           print("DASAD",user_obj.name)
           if user_obj:
              user_obj.status=True
              user_obj.save()
              return Response({'your email has been successfully verified'})
          
    






def t():
    
    
    def get( self , request , pk = None  ,id = None  , *args , **kwargs ):
        if pk == 'user' :
            user = get_object_or_404(sign ,  id = str(id) )
            data = LikeModel.objects.select_related('user' ).prefetch_related('videos').get( Q(user = user) )
            serializer = LikeModelSerializer( data )
            return Response({'status':'success','data':serializer.data },status=status.HTTP_200_OK)
        elif pk == 'video' :
            video_obj = get_object_or_404( detail ,  videoid = str(id) )
            data = LikeModel.objects.prefetch_related('videos').filter( Q( videos = video_obj ) )
            serializer = LikeModelSerializer( data  , many=True)
            return Response({'status':'success','data':serializer.data },status=status.HTTP_200_OK)
        return Response({'status':'success','data': "add 'user' or 'video' in your url " },status=status.HTTP_200_OK)

import threading

class LikeApiForUserView(APIView ):
     def get( self , request , pk = None  ,id = None  , *args , **kwargs ):
        if pk == 'user' :
            user = get_object_or_404(sign ,  id = str(id) )
            data = LikeModel.objects.select_related('user' ).prefetch_related('videos').filter( Q(user = user) )
            if data :
                data = data[0]
                serializer = LikeModelSerializer( data )
                return Response({'status':'success','data':serializer.data , 'total_likes' : int(data.total_likes) },status=status.HTTP_200_OK)
            return Response({'status':'not found'},status=status.HTTP_400_BAD_REQUEST)
        elif pk == 'video' :
            video_obj = get_object_or_404( detail ,  videoid = str(id) )
            data = LikeModel.objects.prefetch_related('videos').filter( Q( videos = video_obj ) )
            serializer = LikeModelSerializer( data  , many=True)
            return Response({'status':'success','data':serializer.data  ,  'total_likes' : int(len(data))},status=status.HTTP_200_OK)
        return Response({'status':'success','data': "add 'user' or 'video' in your url "  },status=status.HTTP_200_OK)



# import pandas as pd
# from xlwt import Workbook
# from django.conf import settings
# # dataFrame =
# import os



# #EXCEL WRITTER FUNCTION
# def d():
#     l = ['shuiab' ,'andasr8u' , 'sbw' , 'sgis' , 'sbsis']
#     dataframe1 = pd.read_excel('Sample100.xlsx' , engine="openpyxl")
#     df2 = pd.DataFrame({   'Serial' : ['bxis' ] ,  'Company':['xiksxs'] ,'Employee':['xbsxs'] , 'Discription':['sbsis']  ,  'Leave':['sbsis'  ]})
#     new_data = pd.concat([dataframe1 , df2] )
#     result = pd.ExcelWriter('Sample100.xlsx',  engine="openpyxl" )
    
#     n_data =  new_data.to_excel( result  , Sheet='Sheet1'  , index=False)
#     result.save()
#     print(new_data)
#     return 0

# d=d()

 

def video_id_checker(history  , videoId , time ):
    result=False

    if history == []:
        history=[{"watchtime":time , "videoid":videoId}]
        return None  , history

    for i in range(0 , len(history)):
        result=False
        if 'videoid'  in history[i].keys() and videoId  in history[i].values() :
            history[i]['watchtime'] = time
            break
        else:
            result = True
    return result , history

#_____________________________________UserHistory ___________________________

class   UserHistoryView( APIView ):
    parser_classes = (JSONParser,)
    def get( self , request , pk = None  , *args , **kwargs ):

        if pk is not None:
            history_obj = get_object_or_404(User_History ,  id = pk )
            if request.GET.get('deleteAllHistory')  == 'True':
                history_obj.history.clear()
                history_obj.save()
            
            serializer = User_Historyserializer( history_obj )
            return Response({'status':'success','data':serializer.data},status=status.HTTP_200_OK)
        all_history_obj  = User_History.objects.all()
        serializer = User_Historyserializer( all_history_obj , many=True )
        return Response({'status':'success','data':serializer.data },status=status.HTTP_200_OK)


    def patch(self,request,pk= None, *args , **kwargs ) :
        if pk is not None:
            queryset = get_object_or_404(User_History ,  id = pk )
            old_history = queryset.history
            
            watchtime = request.data.get('watchtime')
            videoId =  request.data.get('videoid')
            
            result , data = video_id_checker(old_history , videoId , watchtime )
            video_obj = detail.objects.get(id=int(videoId))
            if  not result :
                data[0]['title'] ,  data[0]['file'] , data[0]['tags']  , data[0]['skills'] , data[0]['publish'] , data[0]['published_on'] = video_obj.title ,  str(video_obj.file.url) ,  video_obj.tags , video_obj.skills , video_obj.publish , str(video_obj.published_on)
                old_history = data
                
            elif result or result==None:
                new_data = {'watchtime' :watchtime , 'videoid' :videoId , 'title' : video_obj.title , 'file' :str(video_obj.file.url) , 
                                    'tags' : video_obj.tags , 'skills' : video_obj.skills , 'publish' : video_obj.publish , 'published_on' : str(video_obj.published_on) }
                old_history.append(new_data)
            else:
                pass
            queryset.history  = old_history
            queryset.save()
            serializer = User_Historyserializer( queryset )
            return Response({'status':'success','data':serializer.data},status=status.HTTP_200_OK)
                
           
            
            
    def delete( self, request, pk= None, *args , **kwargs ):
        if pk is not None:
            queryset =  get_object_or_404(User_History ,  id = pk )
            if queryset.exists():
                queryset.delete()
            return Response({'status':'deleted' },status=status.HTTP_200_OK)
        return Response({'status':'fail','data':"DoesNotExist"},status=status.HTTP_400_BAD_REQUEST) 





def word_splitter(query):
    query_list  , length_of_query , count , min_word_limit , word_interval = [] , len(query) , 0 , 5 , 2
    while min_word_limit < length_of_query :
        query_list.append(query[:min_word_limit])
        min_word_limit+=word_interval
    return query_list

def words_finder_in_history(userid , query_list):
    a , results = User_History.objects.get(user = userid) ,  []
    for i in a.history:   
        for words in query_list:
            if i['tags'] and i['skills'] is None:
                if words.replace(' ' , '') in i['title'].replace(' ' , ''):
                    if i not in results:
                        results.append(i)
            if i['tags'] is None:
                if words.replace(' ' , '') in i['skills']  or words.replace(' ' , '') in i['title'].replace(' ' , ''):
                    if i not in results:
                        results.append(i)
            if i['skills'] is None:
                if words.replace(' ' , '') in i['tags']  or words.replace(' ' , '') in i['title'].replace(' ' , ''):
                    if i not in results:
                        results.append(i)
            if words.replace(' ' , '') in i['tags']  or words.replace(' ' , '') in i['title'].replace(' ' , '') or words.replace(' ' , '') in i['skills'].replace(' ' , ''):
                    if i not in results:
                        results.append(i)
    return results

import json


#________________________UserHistorySearch 
class   UserHistorySearchView( APIView ):
    parser_classes = (JSONParser,)
    def get( self , request , pkUser = None  ,*args , **kwargs ):
        if pkUser  is not None:
            query = request.GET.get('searchquery').strip()
            if len(query) > 9:
                all_split_query_words = word_splitter(query)
                final_result = words_finder_in_history(pkUser , all_split_query_words)
                print(all_split_query_words)
                return Response({'status':'success','data':final_result },status=status.HTTP_200_OK)
            



#_________________History to store only 5 same video on Single Day
data = [{'userid' :sign.objects.first().id , 'ipaddress':"123" , 'date' :date.today()} , {'userid' :sign.objects.first().id ,  'ipaddress':"123" ,  'date' :date.today()} , {'userid' :sign.objects.first().id ,  'ipaddress':"123" ,  'date' :date.today()}   ]
new_data= {'userid' :sign.objects.first().id , 'ipaddress':"123" , 'date' :date.today()}
if new_data  not in data:
        data.append(new_data)
else:
    if data.count(new_data) >= 3:
        pass
    else:
        data.append(new_data)



    





