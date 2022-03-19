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
from myapp.forms import CommentForm
from django import http
from django.views.generic.base import View
from datetime import datetime
from django.core.exceptions import ObjectDoesNotExist
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

    
#Add the comment likes and comment dislikes for video

class Addcomment_likes(LoginRequiredMixin,View):
    def video_comment(self,request, id,pk,*args,**kwargs): #id is vedio id ,pk is comment id
        comment=Comment.objects.get(pk=pk)
        is_dislike=False
        for dislike in comment.dislikes.all():
            if dislike == request.user:
                is_dislike=True
                break

        if is_dislike:
            comment.dislikes.remove(request.user)

        is_like=False
        for like in comment.like.all():
            if like==request.user:
                is_like=True
                break

        if not is_like:
            comment.likes.add(request.user)

        if is_like:
            comment.likes.remove(request.user)


        next= request.POST.get('next','/')
        return HttpResponseRedirect(next)


#Add the function comment_dislikes
class Add_dislikecomment(LoginRequiredMixin,View):
    def video_comment(self,request,id,pk,*awargs,**kwargs):
        comment=Comment.objects.get(pk=pk)

        is_like=False
        for like in comment.likes.all():
            if like==request.user:
                is_like=True
                break

        if is_like:
            comment.likes.remove(request.user)

        is_dislike=False

        for dislike in comment.dislikes.all():
            if dislike==request.user:
                is_dislike=True
                break

        if not is_dislike:
            comment.dislikes.add(request.user)

        if is_dislike:
            comment.dislikes.remove(request.user)

        next = request.POST.get('next', '/')
        return HttpResponseRedirect(next)

# function which post the comment and replies comment
def post_detail(request, videofile):
    post = get_object_or_404(videos, slug=videofile)
    comments = post.comments.filter(active=True, parent__isnull=True)
    if request.method == 'POST':
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            parent_obj = None
            try:
                parent_id = int(request.POST.get('parent_id'))
            except:
                parent_id = None
            if parent_id:
                parent_obj = Comment.objects.get(id=parent_id)
                if parent_obj:
                    reply_comment = comment_form.save(commit=False)
                    reply_comment.parent = parent_obj
            new_comment = comment_form.save(commit=False)
            new_comment.post = post
            new_comment.save()
            return HttpResponseRedirect(post.get_absolute_url())
    else:
        comment_form = CommentForm()
        context={'post': post,
                   'comments': comments,
                   'comment_form': comment_form}
    return render(request,
                  'templatename',context)

#function for the follow,unfollow,pending request and delete request.
#function for the follow ,unfollow and pending request and private account
'''
class followUnfollow(APIView):
    permission_classes=[IsAuthenticated]

    def current_profile(self,pk):
        try:
            return Support.objects.get(user=self.request.user)
        except Support.DoesNotExist:
            raise Http404
    
    def other_profile(self,pk,request):
        pk=request.data.get('id')  #here pk is opposite user,s profile ID
        req_type= request.data.get('type')
        current_profile=self.current_profile()
        other_profile=self.other_profile(pk)

        if req_type=='follow':
            if other_profile.private_account:
                other_profile.pending_request.add(current_profile)
                return Response({'Requested':'Follow request has been send !!'},status=status.HTTP_200_0k)

            else:
                if other_profile.blocked_user.filter(id=current_profile).exists():
                    return Response({'Following Fail':"you cannot follow this profilebecuase your id blocked by this user "},status=status.HTTP_400_BAD_REQUEST)
                current_profile.following.add(other_profile)
                other_profile.followers.add(current_profile)
                return Response({"Following":"Following success"},status=status.HTTP_200_0k)

        elif req_type =='accept':
            current_profile.followers.add(other_profile)
            other_profile.following.add(current_profile)
            current_profile.pending_request.remove(other_profile)
            return Response({'Accepted':"Follow request accept successfully"},status=status.HTTP_200_0k)

        elif req_type=='decline':
            current_profile.pending_request.remove(other_profile)
            return Response({'Decline':'follow request successfully declined !!'},status=status.HTTP_200_0k)

        elif  req_type=='unfollow':
            current_profile.following.remove(other_profile)
            other_profile.followers.remove(current_profile)
            return Response({'unfollow':"unfollow success"},status=status.HTTP_200_0k)

        elif req_type=='remove':
            current_profile.followers.remove(other_profile)
            other_profile.following.remove(current_profile)
            return Response({'Remove Success':'Successfully removed your follower'},status=status.HTTP_200_0k)

#here we fetch the data followers,following detail and blocked user
def patch(self,request,format=None):
    req_type=request.data.get('type')

    if req_type=="follow detail":
        serializer=FollowerSerializer(self.current_profile())
        return Response({'data':serializer.data},status=status.HTTP_200_0k)

    elif req_type=='block_pending':
        serializer=BlockPendingSerializer(self.current_profile())
        pf=list(Support.objects.filter(pending_request=self.current_profile().id).values('id','user_username'))
        return Response({'data':serializer.data,'sended Request':pf},status=status.HTTP_200_0k)


#you can block and unblock
def put(self,request,format=None):
    pk=request.data.get('id')
    req_type=request.data.get('type')

    if req_type =='block':
        self.current_profile().blocked_user.add(self.other_profile(pk))
        return Response({'Blocked':'This user blocked successfully '},status=status.HTTP_200_0k)

    elif req_type =='unblock':
        self.current_profile().blocked_user.remove(self.other_profile(pk))
        return Response({'unblocked':"this user unblocked successfully"},status=status.HTTP_200_0k)




#this is useful and alternate for vedio  api

class FileView(APIView):
  parser_classes = (MultiPartParser, FormParser)

  serializer_class=FileSerializer
  
  def get(self,request,id=None):
      if id:
          file=File.objects.get(id=id)
          fileserializer=FileSerializer(file)
          return Response({"status":"success","data":fileserializer.data},status=status.HTTP_200_OK)

      allvideos=File.objects.all()
      serializer=FileSerializer(allvideos,many=True)       #context request:request create the url>>> context={'request':request}
      return Response({ "status":"success","data":serializer.data},status=status.HTTP_200_OK)

  def post(self, request, *args, **kwargs):
    file_serializer = FileSerializer(data=request.data)
    video=request.data.get('file')
    if file_serializer.is_valid():
        cmd=f'ffmpeg -i "{video}" -vf fps=1/6 img%06d.jpg'  
        subprocess.run(cmd, shell=True,stderr=subprocess.STDOUT)
        file_serializer.save()
        return Response({'data':file_serializer.data},status=status.HTTP_201_CREATED)
    else:
      return Response(file_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

  def delete(self, request,  id=None):
        event = get_object_or_404(File,id=id)
        event.delete()
        return Response({"status":"success","data":"item deleted"} )     

'''
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
class SearchAPIView(generics.ListCreateAPIView):
   def get_queryset(self):
        request = self.request
        query = request.GET.get('q', None)
        
        if query is not None:
            blog_results        = detail.objects.search(query)
            lesson_results      = workbaseinfo.objects.search(query)
           
            
            # combine querysets 
            queryset_chain = chain(
                    blog_results,
                    lesson_results,
                   
            )        
            qs = sorted(queryset_chain, 
                        key=lambda instance: instance.pk, 
                        reverse=True)
            self.count = len(qs) # since qs is actually a list
            return qs
        return detail.objects.none() 
#___________________________________________________________________________________________________
class connectSearchAPIView(generics.ListCreateAPIView):
    search_fields = ['^title','^tags','user__name']
    filter_backends = (filters.SearchFilter,)
    queryset =connect.objects.all()
    serializer_class = connectSerializer


#_________________________________________________________________________________________________________________
#comment system begin
from rest_framework import authentication, permissions
class commentApiView(APIView):
    parser_classes= [JSONParser]
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
   
    def get(self,request,post_id=None):
        if post_id:
            allinfo=connect_comment.objects.get(id=post_id)
            serializer=CommentSerializer(allinfo)
            return Response({'status':'success','serializer':serializer.data},status=status.HTTP_200_OK)
        allbaseinfo=connect_comment.objects.all()
        serializer=CommentSerializer(allbaseinfo,many=True)
        return Response(serializer.data,status=status.HTTP_200_OK)

    def post(self,request,post_id=None):
        post=connect.objects.get(pk=post_id)
        serializer=CommentSerializer(data=request.data)
        if serializer.is_valid(post=post):
            serializer.save()
            return Response({'status':'success','data':serializer.data},status=status.HTTP_200_OK)
        else:
            return Response({'status':'error','data':serializer.errors},status=status.HTTP_400_BAD_REQUEST)
    

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

#ffmpeg_______________________________________________________________________________________________________#
import ffmpeg
import subprocess
#thumbnail 
def query_set():
    video = r"C:\ONORALL\media\file\spider_Dud1tKa.mp4"
    #file=File.objects.get(id=154)
    
    cmd=f'ffmpeg -i "{video}" -vf fps=1/6 img%06d.jpg'  
    print(cmd)
    subprocess.run(cmd, shell=True,stderr=subprocess.STDOUT)
    return Response({'video_thumbnail':video}) 
#query_set()

#compressing video
def compressing_video():
    input = r"C:\Users\user\Downloads\amit2.mp4"
    output = r"C:\Users\user\Downloads\out.mp4"
    #cmd=f'ffmpeg -i "{input}" "{output}"'
    cmd=f'ffmpeg -i "{input}" -vcodec libx264 -crf 28 "{output}"'
    print(cmd)
    subprocess.check_output(cmd, shell=True)
#comprressing_video()

#________________________________________________________________________________________________________________#
#likes view

class LikeView(APIView):
    """Toggle like"""

    def get(self, request,like='', format=None, post_id=None):
        post = connect.objects.get(id=post_id)
        user = self.request.user
        #like=True
        if request.user.is_authenticated:
            like=True
            if user in post.likes.all():
                like = False
                post.likes.remove(user)
            else:
                like = True
                post.likes.add(user)
        return Response({'like':like})

#________________________________________________________________________________________________________________________
#for the video toggel like 
class videolikeAPi(APIView):
    def get(self,request,format=None,detid=None):
        video=detail.objects.get(id=detid)
        user=self.request.user
        if request.user.is_authenticated:
            if user in video.likesvideo.all():
                like=False
                video.likesvideo.remove(user)
            else:
                like=True
                video.likesvideo.add(user)
        data={
            'like':like
        }
        return Response(data)
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
            serializer=basic_display_serializer(event)
            return Response({'status':'success','data':serializer.data},status=status.HTTP_200_OK)
        event=basic_display.objects.all()
        serializer=basic_display_serializer(event,many=True)
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
   # print(data)
    converted_data=int(float(data))
    result=converted_data//4
    #frameduration=print(result)
    #print(type(result))
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
    #auto_thumbnail_path=str(output)
    #data=auto_thumbnail_path[:-4]
    #print(data)
    command=f'ffmpeg -i "{video}" -vf fps=1/{frame} {output}img%0d.jpg'  
    #print(command)
    subprocess.run(command, shell=True,stderr=subprocess.STDOUT)
    return Response({'video_thumbnail':video})
a='1O7oaSB2C86m'
#Automatic_generated_thumbnail(a)
#_______________________________________________________________________________________________________________________
def compressing_video(videoid=None):
    file=detail.objects.get(videoid=videoid)
    filepath=str(file)
    print(filepath)
    video=r"C:\ONORALL\media\\" + filepath
    print(video)
    a='1'
    output = r"C:\ONORALL\media\upload\\" + videoid + '\\'+ videoid +'compress.mp4'
    #data=output[:-4]
    cmd=f'ffmpeg -i "{video}" -vcodec libx264 -crf 28 "{output}"' #crf is the most important thing (constant rate factor)
    print(cmd)
    subprocess.check_output(cmd, shell=True)
#videoid="1O7oaSB2C86m"
#compressing_video(videoid)
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

from drf_multiple_model.views import ObjectMultipleModelAPIView  
class SearchFilterView(ObjectMultipleModelAPIView):
    querylist = (
            {'queryset': detail.objects.all(), 'serializer_class': DetailSerializer},
            #{'queryset': workbaseinfo.objects.filter(workbasename='sumitkeen'), 'serializer_class': workserializer},
        )
    filter_backends = (filters.SearchFilter,)
    search_fields = ['title']
#new coomit
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
