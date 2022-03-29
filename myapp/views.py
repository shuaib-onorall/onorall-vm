import json
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
from datetime import datetime
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


#___________________________________________________________________________________________________________________________________________

#Api for video detailing  
class DetailAPIview(APIView):
    pareser_class=[JSONParser]
    #parser_classes = (MultiPartParser, FormParser)
    serializer=DetailSerializer

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
            serializer.save()
            return Response(serializer.data,status=status.HTTP_200_OK)
        else:
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
        else:
            return Response({'status':"error",'data':serializer.errors})

    def delete(self,request,id=None):
        event=get_object_or_404(detail,id=id)   
        event.delete()
        return Response({'status':'success','data':'items deleted'}) 
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
        
        allposts=connect.objects.all()
        serializer=connectSerializer(allposts,many=True)
        return Response(serializer.data,status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        doc_serializer = connectSerializer(data=request.data)
        if doc_serializer.is_valid():
            doc_serializer.save()
            return Response(doc_serializer.data, status=status.HTTP_201_CREATED)
        else:
          return Response(doc_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self,request,id=None):
        post=connect.objects.get(id=id)
        serializer=connectSerializer(post,data=request.data,partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({'status':'success','data':serializer.data})
        else:
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
    #parser_classes = (MultiPartParser, FormParser)
    serializer_class=tag

    def get(self,request,id=None):
        if id:
            allpost=section.objects.get(id=id)
            serializer=tag(allpost)
            return Response({'status':'success','data':serializer.data},status=status.HTTP_200_OK)
        
        allposts=section.objects.all()
        serializer=tag(allposts,many=True)
        return Response(serializer.data,status=status.HTTP_200_OK)

    def post(self,request,*args, **kwargs):
        serializer=tag(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
          return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self,request,id=None):
        about=section.objects.get(id=id)
        serializer=tag(about,data=request.data,partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({'status':'success','data':serializer.data})
        else:
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
    parser_classes = [JSONParser]

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
        serializer=signserializers(data=request.data)
        gmail=request.data.get('gmail')
        phone=request.data.get('phone')
        profile_mail=sign.objects.filter(gmail=gmail).exists()
        if not serializer.is_valid():
            return Response({'status':403,'error':serializer.errors})
        serializer.save()
        if profile_mail:
            return Response({'status':'gmail  already exist'})
        if phone:
            user=sign.objects.get(phone=serializer.data['phone'])
            refresh = RefreshToken.for_user(user) #this line important for jwt token
            return Response({'status':200,'payload':serializer.data,'refresh':str(refresh),'access':str(refresh.access_token)})
        return Response({'status':200,'payload':serializer.data})

    def patch(self,request,id=None):
        post=sign.objects.get(id=id)
        serializer=signserializers(post,data=request.data,partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({'status':'success','data':serializer.data})
        else:
            return Response({'status':"error",'data':serializer.errors})


    def delete(self, request,  id=None):
        event = get_object_or_404(sign,id=id)
        event.delete()
        return Response({"status":"success","data":"item deleted"} ) 

#____________________________________________________________________________________________________
    

#api for groupskills
class grouplistAPIView(APIView):
    parser_classes= [JSONParser]
    playlist_serializer=groupserializer

    def get(self,request,id=None):
        if id:
            allplaylist=group.objects.get(id=id)
            serializer=groupserializer(allplaylist)
            return Response({'status':'success','serializer':serializer.data},status=status.HTTP_200_OK)
        allplaylist=group.objects.all()
        serializer=groupserializer(allplaylist,many=True)
        return Response({'status':'success','list_of_playlist':serializer.data,},status=status.HTTP_200_OK)

    def post(self,request):
        playlist_serializer=groupserializer(data=request.data)
        if playlist_serializer.is_valid():
            playlist_serializer.save()
            return Response(playlist_serializer.data,status=status.HTTP_200_OK)
        else:
            return Response(playlist_serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    
    def patch(self,request,id=None):
        list=group.objects.get(id=id)
        serializer=groupserializer(list,data=request.data,partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({'status':'success','data':serializer.data})
        else:
            return Response({'status':'error','data':serializer.error})

    def delete(self,request,id:None):
        event=get_object_or_404(group,id=id)
        event.delete()
        return Response({'status':'deleted'})



#playlist api
class playlistAPIView(APIView):
    parser_classes= (MultiPartParser, FormParser)
    def get(self,request,id=None,vid=None):
        if id:
            allplaylist=playlist.objects.get(id=id)
            serializer=playlist_videoserializer(allplaylist)
            if vid:
                file=detail.objects.get(id=vid)
                fileserializer=DetailSerializer(file)
                return Response({'data':fileserializer.data})
           
            return Response({'status':'success','serializer':serializer.data},status=status.HTTP_200_OK)
        allplaylist=playlist.objects.all()
        serializer=playlist_videoserializer(allplaylist,many=True)
        return Response({'status':'success','list_of_playlist':serializer.data,},status=status.HTTP_200_OK)

    def post(self,request):
        serializer=playlist_videoserializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'status':'success','data':serializer.data},status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
#_______________________________________________________________________________________________________________________
#workbase api
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
        work=workbaseinfo.objects.filter(workbasename=workbasename).exists()
        if work:
            return Response({'status':'workbasename already exist'})
        if serializer.is_valid():
                serializer.save()
                return Response({'status':'success','data':serializer.data},status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

    def patch(self,request,id=None):
        post=workbaseinfo.objects.get(id=id)
        serializer=workserializer(post,data=request.data,partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({'status':'success','data':serializer.data})
        else:
            return Response({'status':"error",'data':serializer.errors})

    def delete(self, request,  id=None):
        event = get_object_or_404(workbaseinfo,id=id)
        event.delete()
        return Response({"status":"success","data":"item deleted"} ) 

#_____________________________________________________________________________________________________________________

#wokred on search on functionality'
from itertools import chain
from rest_framework import filters
from rest_framework import generics
#_______________________________________________________________
class connectSearchAPIView(generics.ListCreateAPIView):
    search_fields = ['^title','^tags','user__name']
    filter_backends = (filters.SearchFilter,)
    queryset =connect.objects.all()
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
            conn.request("GET", "https://2factor.in/API/V1/7c1b03c3-7905-11ec-b710-0200cd936042/SMS/+91"+phone+"/AUTOGEN") 
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
    serializer=addresourceserializer
    def get(self,request,id=None):
        if id:
            reportinfo=Addresources.objects.get(id=id)
            serializer_info=addresourceserializer(reportinfo)
            return Response(serializer_info.data,status=status.HTTP_200_OK)

        report_info=Addresources.objects.all()
        report_serializer=addresourceserializer(report_info,many=True)
        return Response(report_serializer.data,status=status.HTTP_200_OK)

    def post(self,request,*args,**kwargs):
        serializer=addresourceserializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_200_OK)
        else:
            return Response({'data':serializer.errors},status=status.HTTP_400_BAD_REQUEST)

    def delete(self,request,id=None):
        event=get_object_or_404(Addresources,id=id)
        event.delete()
        return Response({'status':'deleted','data':'item deleted'})

#___________________________________________________________________________________________________________________
class questionnaireAPIView(APIView):
    parser=(MultiPartParser,FormParser)
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
        serializer=questionnaireserializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return response({'status':'success','data':serializer.data},status=status.HTTP_200_OK)
        else:
            return Response({'status':'success','data':serializer.data},stauts=status.HTTP_200_OK)
    
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
            info=question.objects.get(ques1id=ques1id)
            serializer=question1serializer(info)
            return Response(serializer.data,status=status.HTTP_200_OK)
        
        info=question.objects.all()
        serializer=question1serializer(info,many=True)
        return Response(serializer.data,status=status.HTTP_200_OK)

    def post(self,request,*args,**kwargs):
        serializer=question1serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'status':'success','data':serializer.data},status=status.HTTP_200_OK)
        else:
            return Response({'status':'fail','data':serializer.errors},status=status.HTTP_400_BAD_REQUEST)
    
    def patch(self,request,id=None):
        event=question.objects.get(ques1id=id)
        serializer=question1serializer(event,data=request.data,partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({'status':'success','data':serializer.data},status=status.HTTP_200_OK)
        else:
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
        
        info=question2.objects.all()
        serializer=question2serializer(info,many=True)
        return Response(serializer.data,status=status.HTTP_200_OK)

    def post(self,request,*args,**kwargs):
        serializer=question2serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'status':'success','data':serializer.data},status=status.HTTP_200_OK)
        else:
            return Response({'status':'fail','data':serializer.errors},status=status.HTTP_400_BAD_REQUEST)
    
    def patch(self,request,id=None):
        event=question2.objects.get(id=id)
        serializer=question2serializer(event,data=request.data,partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({'status':'success','data':serializer.data},status=status.HTTP_200_OK)
        else:
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
            info=question3.objects.get(id=id)
            serializer=question3serializer(info)
            return Response(serializer.data,status=status.HTTP_200_OK)
        
        info=question3.objects.all()
        serializer=question3serializer(info,many=True)
        return Response(serializer.data,status=status.HTTP_200_OK)

    def post(self,request,*args,**kwargs):
        serializer=question3serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'status':'success','data':serializer.data},status=status.HTTP_200_OK)
        else:
            return Response({'status':'fail','data':serializer.errors},status=status.HTTP_400_BAD_REQUEST)
    
    def patch(self,request,id=None):
        event=question3.objects.get(id=id)
        serializer=question3serializer(event,data=request.data,partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({'status':'success','data':serializer.data},status=status.HTTP_200_OK)
        else:
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
            info=abc.objects.get(id=id)
            serializer=UserSerializer(info)
            return Response(serializer.data,status=status.HTTP_200_OK)
        
        info=abc.objects.all()
        serializer=UserSerializer(info,many=True)
        return Response(serializer.data,status=status.HTTP_200_OK)

    def post(self,request,*args,**kwargs):
        serializer=UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'status':'success','data':serializer.data},status=status.HTTP_200_OK)
        else:
            return Response({'status':'fail','data':serializer.errors},status=status.HTTP_400_BAD_REQUEST)
    
    def patch(self,request,id=None):
        event=abc.objects.get(id=id)
        serializer=UserSerializer(event,data=request.data,partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({'status':'success','data':serializer.data},status=status.HTTP_200_OK)
        else:
            return Response({'status':'success','data':serializer.errors})
#_______________________________________________________________________________________________________________________

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
        else:
            return Response({'status':'fail','data':serializer.errors},status=status.HTTP_400_BAD_REQUEST)
        
    def patch(self,request,id=None):
        event=basic_display.objects.get(id=id)
        serializer=basic_display_serializer(event,data=request.data,partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({'status':'success','data':serializer.data},status=status.HTTP_200_OK)
        else:
            return Response({'status':'fail','data':serializer.errors},status=status.HTTP_400_BAD_REQUEST)
            

class basic_brandingAPIView(APIView):
    parser=(MultiPartParser,FormParser)
    def get(self,request,id=None):
        if id:
            event=basic_branding.objects.get(id=id)
            serializer=basic_branding_serializer(event)
            return Response({'status':'success','data':serializer.data},status=status.HTTP_200_OK)
        event=basic_branding.objects.all()
        serializer=basic_branding_serializer(event,many=True)
        return Response({'status':'success','data':serializer.data},status=status.HTTP_200_OK)
    
    def post(self,request,*args,**kwargs):
        serializer=basic_branding_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'status':'success','data':serializer.data},status=status.HTTP_200_OK)
        else:
            return Response({'status':'fail',"data":serializer.errors},status=status.HTTP_400_BAD_REQUEST)

    def patch(self,request,id=None):
        event=basic_branding.objects.get(id=id)
        serializer=basic_branding_serializer(event,data=request.data,partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({'status':'success','data':serializer.data},status=status.HTTP_200_OK)
        else:
            return Response({'status':'fail','data':serializer.errors},status=status.HTTP_400_BAD_REQUEST) 

#_______________________________________________________________________________________________________________________

class exAPIView(APIView):
    parser_classes = [JSONParser]
  
    serializer_class=workserializer
    def get(self,request,workbasename=None):
        if workbasename:
            allinfo=workbaseinfo.objects.get(workbasename=workbasename)
            serializer=workserializer(allinfo)
            return Response({'status':'success','serializer':serializer.data},status=status.HTTP_200_OK)
        allbaseinfo=workbaseinfo.objects.all()
        serializer=workserializer(allbaseinfo,many=True)
        return Response({'status':'success','data':serializer.data},status=status.HTTP_200_OK)
#__________________________________________________________________________________________________________________________
class APIView(APIView):
    parser_classes = [JSONParser]
  
    serializer_class=fileserializer
    def get(self,request,id=None,name=None):
        if id:
            allinfo=MyModel.objects.get(id=id)
            if name:
                allinfo=MyModel.objects.get(name=name)
                serializer=fileserializer(allinfo) 
                return Response({'status':'success','serializer':serializer.data},status=status.HTTP_200_OK)
        allbaseinfo=MyModel.objects.all()
        serializer=fileserializer(allbaseinfo,many=True)
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
    a='1'
    output = r"C:\ONORALL\media\upload\\" + videoid + '\\'+ videoid +'compress.mp4'
    cmd=f'ffmpeg -i "{video}" -vcodec libx264 -crf 28 "{output}"' #crf is the most important thing (constant rate factor)
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
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#___________________________________________________________________________________________________________________________


#________________________________________________________________________________________________________________________________
class supportAPI(APIView):
    def get(self,request,id=None):
        if id:
            support=Support.objects.get(id=id)
            serializer=supportserializers(support)
            return Response({'data':serializer.data,'status':'success'},status=status.HTTP_200_OK)
        support=Support.objects.all()
        serializer=supportserializers(support,many=True)
        return Response({'data':serializer.data},status=status.HTTP_200_OK)

    def post(self,request):
        serializer=supportserializers(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'data':serializer.data},status=status.HTTP_200_OK)
        else:
            return Response({'status':'fail','data':serializer.errors},status=status.HTTP_400_BAD_REQUEST)

    def delete(self,request,id=None):
        event=get_object_or_404(Support,id=id)
        event.delete()
        return Response({'item deleted'})

#_______________________________________________________________________________________________________________________________________
class multitablesearch(APIView):
    def get( self , request , title = None  , *args , **kwargs ):
        combine_query = {}
        if title is not None:
            title=title.lower().strip()
            detail_obj = detail.objects.filter( title__icontains = title )
            serializer = DetailSerializer( detail_obj  , many=True)
            combine_query[' detail result '] = serializer.data 

            workbase_obj = workbaseinfo.objects.filter( workbasename__icontains = title )
            serializer1 = workserializer( workbase_obj , many = True)
            combine_query[' workbase result '] = serializer1.data

            return Response({'status':'success','data':combine_query },status=status.HTTP_200_OK)
        return Response({'status':'fail','data':"provide query in url"},status=status.HTTP_400_BAD_REQUEST) 

#______________________________________________________________________________________________________________________________________
class connect_comment_Api(APIView):
    def get(self,request,id=None):
        if id:
            comment=connect_comment.objects.get(id=id)
            serializers=connect_comment_serializer(comment)
            return Response({'data':serializers.data,'status':'success'},status=status.HTTP_200_OK)
        comment_data=connect_comment.objects.all()
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

    def put(self, request, pk=None , format=None):
        if pk is not None:
            obj = connect_comment.objects.get( id = pk)
            if request.data['action'] == "like" :
                new_ids = request.data.get('likes_comment')   
                if new_ids != None:                  
                    sign_obj = sign.objects.get(id=str(new_ids[0]))               
                    if sign_obj not in obj.likes_comment.all() :              
                        obj.likes_comment.add(sign_obj)
                        obj.like_active ='liked'
                        obj.save()
                        if sign_obj in obj.comment_dislikes.all():
                            obj.comment_dislikes.remove(sign_obj)
                            obj.dislike_active ='null'
                            obj.save()
                            serializer = connect_comment_serializer(obj)
                            return Response({'status':'removelike-success','data':serializer.data},status=status.HTTP_200_OK)
                        serializer = connect_comment_serializer(obj)
                        return Response({'status':'removelike-success','data':serializer.data},status=status.HTTP_200_OK)
                    else:
                        obj.likes_comment.remove(sign_obj)
                        obj.like_active = 'null'
                        obj.save()
                        serializer = connect_comment_serializer(obj)
                        return Response({'status':'removelike-success','data':serializer.data},status=status.HTTP_200_OK)
                serializer = connect_comment_serializer(obj)
                return Response({'status':'removelike-success'},status=status.HTTP_200_OK)    
            elif request.data['action'] == "dislike" :
                new_ids = request.data.get('comment_dislikes') 
                if new_ids != None:                  
                    sign_obj = sign.objects.get(id=str(new_ids[0]))
                    if sign_obj in obj.comment_dislikes.all():
                        obj.comment_dislikes.remove(sign_obj)
                        obj.dislike_active = 'null'
                        obj.save()
                        serializer = connect_comment_serializer(obj)
                        return Response({'status':'removelike-success','data':serializer.data},status=status.HTTP_200_OK)
                    else:
                        obj.comment_dislikes.add(sign_obj)
                        obj.dislike_active ='disliked' 
                        obj.save() 
                        if sign_obj in obj.likes_comment.all():
                            obj.likes_comment.remove(sign_obj)
                            obj.like_active ='null'
                            obj.save()
                            serializer = connect_comment_serializer(obj)
                            return Response({'status':'removelike-success','data':serializer.data},status=status.HTTP_200_OK)
                        serializer = connect_comment_serializer(obj)
                        return Response({'status':'removelike-success','data':serializer.data},status=status.HTTP_200_OK)
                serializer = connect_comment_serializer(obj)
                return Response({'status':'removelike-success'},status = status.HTTP_200_OK)


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
