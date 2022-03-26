from distutils.command.upload import upload
from enum import unique
from tabnanny import verbose
from unittest.mock import DEFAULT
from django.db import models
from django.contrib.auth.models import User
from django.forms import CharField
from django.urls import reverse
from django.contrib.auth.models import User
import uuid
from django.contrib.contenttypes.fields import GenericForeignKey

import random, string

def random_id_field():
  rnd_id = ''.join(random.choices(string.ascii_letters + string.digits, k=12))
  return rnd_id


#_______________________________________________________________________________________________________________________
#user model
class sign(models.Model):
    id = models.CharField(max_length=12, unique=True, primary_key=True,  default=random_id_field)
    name=models.CharField(max_length=30)
    phone=models.CharField(max_length=13,null=True,blank=True)
    gmail=models.EmailField(null=True,blank=True)
    iscreator=models.BooleanField(default=False)
   
    def __str__(self):
        return str(self.id)

#____________________________________________________________________________________________________________________

#models for workbase
workbase_choices=(
    ('show my skills','show my skills'),
    ('Recruit candidate','Recruit candidate'),
    ('Startup(skills+Recruit)','Startup(skills+Recruit)'),
)
class workbaseinfo(models.Model):
    wbid = models.CharField(max_length=12, unique=True,default=random_id_field)
    userid=models.ForeignKey(sign,on_delete=models.CASCADE)
    workbasename=models.CharField(max_length=25,blank=True,null=True)
    workbasechoices=models.CharField(max_length=30,choices=workbase_choices,default='show my skills')
    wbemail=models.EmailField(null=True,blank=True)
    wbdescription=models.TextField(null=True,blank=True)
    location=models.CharField(max_length=30)
    
    def __str__(self):
        return str(self.workbasename)



#______________________________________________________________________________________________________________________
 #for the videos detailing
def get_upload_to(instance, videoid):
    return 'upload/%s/%s' % (instance.videoid,videoid)


def create_url( videoid):
    return 'http://192.168.1.85:8000/general/' +(videoid) #this is used of rsutom thumbnail 


publish_choices=(  #this will used for choice in community.
    ('public','public'),
    ('private','private'),
    ('unlist','unlist'),
    
)
target_choice=(
    ('not-for-kids','not-for-kids'),
    ('kids','kids'),
)
age_restriction_choice=(
    ('no-restrict','no-restrict'),
    ('restrict','restrict'),
)
class detail(models.Model):
    videoid = models.CharField(max_length=12, unique=True,   default=random_id_field)
    user_id=models.ForeignKey(sign,null=True,blank=True,on_delete=models.CASCADE)
    title=models.CharField(max_length=50,null=True,blank=True)
    file=models.FileField(upload_to=get_upload_to)
    description=models.TextField(null=True,blank=True)
    customthumbnail=models.ImageField(upload_to=get_upload_to,null=True,blank=True,verbose_name='customthumbnail')
    tags=models.CharField(max_length=500,null=True,blank=True)
    skills=models.CharField(max_length=500,null=True,blank=True)
    compress=models.BooleanField(default=False)
    targetaudience=models.CharField(max_length=100,choices=target_choice,default='not-for-kids')
    agerestriction=models.CharField(max_length=100,choices=age_restriction_choice,default='no-restrict')
    isCommentsOn=models.BooleanField(default=True)
    isLikeCountOn=models.BooleanField(default=True)
    isAudioCommentOn=models.BooleanField(default=True)
    likesvideo=models.ManyToManyField(sign,related_name='likes',blank=True,default=None)
    publish=models.CharField(max_length=100,choices=publish_choices,default='public')
    published_on=models.DateField(auto_now=True)

    
    @property
    def total_likes(self):
        return self.likesvideo.all().count()

    def __str__(self) -> str:
        return  f"ID : {str(self.id)} || {str(self.title)}"
    

#_______________________________________________
class timelineModel(models.Model):
    time = models.CharField(max_length=200)
    user_id=models.ForeignKey(sign,null=True,blank=True,on_delete=models.CASCADE)
    resourcesid = models.CharField(max_length=12, unique=True,   default=random_id_field)
    resourcesfile=models.FileField(upload_to='resources/',null=True,blank=True)
    connected_to = models.ForeignKey(detail , on_delete=models.CASCADE)
    
    def __str__(self) -> str:
        return  f"ID : {str(self.id)} || USER_ID : {str(self.user_id)}"


#___________________________________________________________________________________________________________________________

#this model is used for document verification   (integerated with frontend)
class doc_verification(models.Model):
    docid = models.CharField(max_length=12, unique=True,   default=random_id_field)
    user_id=models.ForeignKey(sign,on_delete=models.CASCADE)
    firstname=models.CharField(max_length=10)
    lastname=models.CharField(max_length=10)
    email=models.EmailField(unique=True)
    qualification=models.CharField(max_length=10,default='')
    specialized=models.CharField(max_length=15,default='')
    skill_tags=models.CharField(max_length=500)
    year_of_experience=models.PositiveIntegerField()
    #document_upload=models.FileField(upload_to='document/',null=True,blank=True,verbose_name='document_upload')
    #upload_photo=models.ImageField(upload_to='photo/',null=True,blank=True,verbose_name='upload_photo')


    def __str__(self):
        return str(self.firstname) +''+str(self.lastname)

#____________________________________________________________________________________________________________
#models for connect section 
publish_choices=(  #this will used for choice in community.
    ('public','public'),
    ('private','private'),
    ('unlist','unlist'),
    
)

class connect(models.Model):
    connectid = models.CharField(max_length=12, unique=True,   default=random_id_field)
    user = models.ForeignKey(sign ,on_delete=models.CASCADE)
    connect=models.ImageField(upload_to='post/',null=True,verbose_name='connect')
    title=models.CharField(max_length=50)
    tags=models.CharField(max_length=100)
    published_on=models.CharField(max_length=100,choices=publish_choices,default='public')
    likes=models.ManyToManyField(User,blank=True,related_name='likes')
   
   
    def number_of_likes(self):
        if self.likes.count():
            return self.likes.count()
        else:
            return 0

    def __str__(self):
        return str(self.title)
#_________________________________________________________________________________________________________________________


#community post comment
class connect_comment(models.Model):
    commentid = models.CharField(max_length=12, unique=True,   default=random_id_field)
    user=models.ForeignKey(sign,blank=True,on_delete=models.CASCADE)
    post_comment=models.TextField()
    post_created_on=models.DateTimeField(auto_now=True)
    post=models.ForeignKey(connect,blank=True,on_delete=models.CASCADE)
    parent=models.ForeignKey('connect_comment',null=True,blank=True,related_name='replies',on_delete=models.CASCADE)
    likes=models.ManyToManyField(User,blank=True ,related_name='Post_comment_likes')
    comment_disllikes=models.ManyToManyField(sign,blank=True,related_name='Post_comment_dislkikes')

    class Meta:
        ordering=['-post_created_on']

    def __str__(self):
        return str(self.post_comment)

    def get_absolute_url(self):
        return reverse('post-detail', kwargs={'pk': self.pk})

    def children(self):
        return connect_comment.objects.filter(parent=self)

    @property
    def is_parent(self):
        if self.parent is not None:
            return False
        return True

#______________________________________________________________________________________________________________________________

class videos(models.Model):
    #id=models.AutoField(primary_key=True)
    id=models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    VideoTitle=models.CharField(max_length=50)
    VideoFile= models.FileField(upload_to='videos/', null=True, verbose_name="video_upload")
    published_date=models.DateTimeField(auto_now=True)
    likes=models.ManyToManyField(User,related_name='videos')
    Description=models.TextField(max_length=5000)
    active_earn=models.PositiveIntegerField(default=0)
    views=models.ManyToManyField(User,related_name='video_views')
    Add_tags=models.CharField(max_length=300,default=0)
    skillcategory=models.CharField(max_length=50,default=0)
    skills=models.CharField(max_length=500,default=0)
    groupskills=models.CharField(max_length=500,default=0)
    Targeting_Audience=models.PositiveIntegerField(default=0)
    Age_restiction=models.PositiveIntegerField(default=0)
    supported=models.PositiveIntegerField(default=0)
    code_mode=models.PositiveIntegerField(default=0)

    @property
    def total_likes(self):
        return self.likes.all().count()

    def total_views(self):
        return self.views.all().count()

    def get_absolute_url(self):
        return reverse("detail",args=[self.id])


    def __str__(self):
        return self.VideoTitle+''+str(self.VideoFile) 
#_________________________________________________________________________________________________________________________

# comment section
class Comment(models.Model):
    #id=models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    vediofile=models.ForeignKey(videos, related_name='comment', on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE,null=True)
    comment=models.TextField()
    parent=models.ForeignKey('self',null=True,blank=True,related_name='replies',on_delete=models.CASCADE)
    audio_comment=models.FileField(upload_to='comment/',null=True,verbose_name='')
    created_on=models.DateTimeField(auto_now=True)
    comment_likes=models.ManyToManyField(User,blank=True,related_name='comment_likes')
    comment_disllikes=models.ManyToManyField(User,blank=True,related_name='comment_dislkikes')


    class Meta:
        ordering=['-created_on']  #this will help you in ordering the component


    def __str__(self):
        return str(self.user) #+''+str(self.id)

#____________________________________________________________________________________________________________________
#this model for social handling
class social_handling(models.Model):
    socialid = models.CharField(max_length=12, unique=True,   default=random_id_field)
    social1=models.URLField(max_length=200,null=True,blank=True)
    social2=models.URLField(max_length=200,null=True,blank=True)
    social3=models.URLField(max_length=200,blank=True,null=True)
    social4=models.URLField(max_length=200,blank=True,null=True)
    social5=models.URLField(max_length=200,blank=True,null=True)
   
#______________________________________________________________________________________________________________

#this model for support section
class Support(models.Model):
    user=models.ForeignKey(sign,blank=True,null=True,on_delete=models.CASCADE)
    wbname=models.ForeignKey(workbaseinfo,null=True,blank=True,on_delete=models.CASCADE)
    
    def __str__(self):
        return str(self.user)
#_______________________________________________________________________________________________________________________

#models for About section
class section(models.Model):
    sectionid = models.CharField(max_length=12, unique=True,   default=random_id_field)
    user_profile=models.ForeignKey(sign,blank=True,on_delete=models.CASCADE)
    description=models.CharField(max_length=50000)
    email_id=models.EmailField()
    location=models.CharField(max_length=50)
    published_date=models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.location

#________________________________________________________________________________________________________________

#playlist 
class playlist(models.Model):
    grouplistid = models.CharField(max_length=12, unique=True,   default=random_id_field)
    userid=models.ForeignKey(sign,on_delete=models.CASCADE)
    name=models.CharField(max_length=20)
    files=models.ManyToManyField(detail)

    def __str__(self):
        return str(self.name)
    
#group name
class group(models.Model):
    groupskillid = models.CharField(max_length=12, unique=True,   default=random_id_field)
    userid=models.ForeignKey(sign,null=True,blank=True,on_delete=models.CASCADE)
    title=models.CharField(max_length=30)
    list=models.ManyToManyField(playlist)

    def __str__(self):
        return str(self.title)


    
#________________________________________________________________________________________________________________________

    
#Notification
class Notification(models.Model):
    notice=models.CharField(max_length=30)

    def __str__(self):
        return str(self.notice)

#____________________________________________________________________________________________________________________________

#this model is used for the basic_dsiplay section
class basic_display(models.Model):
    highlightid = models.CharField(max_length=12, unique=True,   default=random_id_field)
    highlight1=models.ForeignKey(detail,related_name='highlight1',null=True,blank=True,on_delete=models.CASCADE)
    highlight2=models.ForeignKey(detail,null=True,related_name='highlight2',blank=True,on_delete=models.CASCADE)
    highlight3=models.ForeignKey(detail,null=True,related_name='highlight3',blank=True,on_delete=models.CASCADE)
    highlight4=models.ForeignKey(detail,null=True,related_name='highlight4',blank=True,on_delete=models.CASCADE)
    highlight5=models.ForeignKey(detail,null=True,related_name='highlight5',blank=True,on_delete=models.CASCADE)

    def __str__(self):
        return str(self.highlight1)

#_______________________________________________________________________________________________________________________

#this model is used for the basic branding
class basic_branding(models.Model):
    brandingid = models.CharField(max_length=12, unique=True,   default=random_id_field)
    userid=models.ForeignKey(sign,on_delete=models.CASCADE)
    wblogo=models.FileField(upload_to='wblogo/',blank=True,null=True)
    banner=models.FileField(upload_to='banner/',blank=True,null=True)

    def __str__(self):
        return str(self.wblogo)

#_____________________________________________________________________________________________________________________
#report
report_choice=(
    ('sexual content','sexual content'),
    ('violent or repulsive content','violent or repulsive content'),
    ('hateful or abusive content','hateful or abusive content'),
    ('harresment or bullyingcontent','harresment or bullyingcontent,'),
    ('hamrful or dangers act','hamrful or dangers act'),
    ('promotes terrorism','promotes terrorism,'),
    ('spam or misleading','spam or misleading'),
    ('infringes my rights','infringes my rights'),
    
)

class report4(models.Model):
    reportid = models.CharField(max_length=12, unique=True,   default=random_id_field)
    report_user=models.ForeignKey(sign,blank=True,on_delete=models.CASCADE)
    report_file=models.ForeignKey(detail,blank=True,on_delete=models.CASCADE)
    report_post=models.ForeignKey(connect,blank=True,on_delete=models.CASCADE)
    report_descript=models.CharField(max_length=100)
    choice=models.CharField(max_length=100,choices=report_choice)

    def __str__(self):
        return str(self.choice)

#____________________________________________________________________________________________________________________________
class questionnaires(models.Model):
    ques_id=models.AutoField(primary_key=True,verbose_name='id')
    questionnaireid = models.CharField(max_length=12, unique=True,   default=random_id_field)
    userid=models.ForeignKey(sign,on_delete=models.CASCADE)
    videoid=models.ForeignKey(detail,on_delete=models.CASCADE)
    description=models.TextField(default='')

    def __str__(self) -> str:
        return str(self.description)

class question(models.Model):
    textid = models.CharField(max_length=12, unique=True,   default=random_id_field)
    ques=models.ForeignKey(questionnaires,null=True,blank=True,on_delete=models.CASCADE)
    question=models.TextField(default='')
    imgfile=models.FileField(upload_to='question/',null=True,blank=True)
    answer=models.TextField(default='')
    isrequired=models.BooleanField(default=True)

    def __str__(self) -> str:
        return str(self.question)



class question2(models.Model):
    qnaid = models.CharField(max_length=12, unique=True,   default=random_id_field)
    questionnaire=models.ForeignKey(questionnaires,null=True,blank=True,on_delete=models.CASCADE)
    question=models.TextField(default='')
    imgfile=models.FileField(upload_to='question2/',null=True,blank=True)
    answer=models.TextField(default='')
    isrequired=models.BooleanField(default=True)

    def __str__(self) -> str:
        return str(self.question)


class question3(models.Model):
    mcqid = models.CharField(max_length=12, unique=True,   default=random_id_field)
    questionnaire=models.ForeignKey(questionnaires,null=True,blank=True,on_delete=models.CASCADE)
    question=models.TextField(default='')
    imgfile=models.FileField(upload_to='question3/',null=True,blank=True)
    option1=models.TextField()
    option2=models.TextField()
    option3=models.TextField()
    option4=models.TextField()
    img1_option=models.FileField(upload_to='question_mcq/img1_option',null=True,blank=True)
    img2_option=models.FileField(upload_to='question_mcq/img2_option',null=True,blank=True)
    img3_option=models.FileField(upload_to='question_mcq/img3_option',null=True,blank=True)
    img4_option=models.FileField(upload_to='question_mcq/img4_option',null=True,blank=True)
    answer=models.CharField(max_length=100,null=True,blank=True,default='')
    isrequired=models.BooleanField(default=False)
    

    def __str__(self) -> str:
        return str(self.question)

class Addresources(models.Model):
    user_id=models.ForeignKey(sign,null=True,blank=True,on_delete=models.CASCADE)
    resourcesid = models.CharField(max_length=12, unique=True,   default=random_id_field)
    video_id=models.ForeignKey(detail,blank=True,null=True,on_delete=models.CASCADE)
    timeline=models.CharField("hr:min:se",max_length=20)
    resourcesfile=models.FileField(upload_to='resources/',null=True,blank=True)
    questionnaire=models.ForeignKey(questionnaires,related_name='questionnaire',null=True,blank=True,on_delete=models.CASCADE)

    def __str__(self) -> str:
        return str(self.timeline)



    

#________________________________________________________________________________________________________
class Contact(models.Model):

    name = models.CharField(max_length=50, blank=True)
    status = models.BooleanField(default=False)



class abc(models.Model):
    username = models.CharField(max_length=50, blank=True)
    password = models.CharField(max_length=50, blank=True)
    skills=models.CharField(max_length=100)
    contact_id = models.ForeignKey(Contact,on_delete=models.CASCADE,related_name='contact_id', blank=True, null=True)

class File(models.Model):
    attr1=models.FileField(upload_to='attr1/')

    def __str__(self) -> str:
        return str(self.attr1)

import random, string

def random_id_field():
  rnd_id = ''.join(random.choices(string.ascii_letters + string.digits, k=16))
  return rnd_id

class MyModel(models.Model):
  myid = models.CharField(max_length=16, unique=True, default=random_id_field)
  ex=models.FileField(upload_to='mymodel1/')
  name=models.CharField(max_length=30)
  

  def __str__(self):
    return str(self.name)
#____________________________________________________________________________________________________________________________

status_choices=(('Invited','Invited'),
                ('Accepted','Accepted'))



class sharemon(models.Model):
    name=models.CharField(max_length=30)
    email=models.EmailField()
    code=models.CharField(max_length=10,blank=True)
    recommended_by=models.OneToOneField(sign,on_delete=models.CASCADE,verbose_name='recommended_by')
    status=models.CharField(max_length=10,choices=status_choices,default='Invited')
    clicked =models.BooleanField(default=False)
    Accountsigned=models.BooleanField(default=False)
    CreatorAccount=models.BooleanField(default=False)
    videoupload=models.BooleanField(default=False)

    def __str__(self) -> str:
        return str(self.name)

    def save(self,*args,**kwargs):
        if self.code=="":
            pass
        super().save(*args,**kwargs)

#_________________________________________________________________________________________________________________________________














# # REPLY FOR COMMENT
# class Reply(models.Model):
#     #reply_id = models.AutoField(primary_key=True  , null=False , blank=False , unique=True )
#     created_time = models.DateTimeField( auto_now_add  = True )
#     person_name = models.ForeignKey( sign  , on_delete = models.CASCADE , related_name="person_name")
#     for_reply =   models.ForeignKey( sign  , on_delete = models.CASCADE , related_name="for_reply")
#     reply_video = models.ForeignKey( detail , on_delete = models.CASCADE )
#     reply_text = models.CharField( max_length = 2000  , default=" ")
    
    
#     def __str__(self):
#         return f"ID : {self.id} || Time : {self.created_time} || personName : {self.person_name}"


# REPLY FOR COMMENT
class Reply(models.Model):
    #reply_id = models.AutoField(primary_key=True  , null=False , blank=False , unique=True )
    created_time = models.DateTimeField( auto_now_add  = True )
    person_id = models.ForeignKey( sign  , on_delete = models.CASCADE , related_name="person_name_1")
    for_reply =   models.ForeignKey( sign  , on_delete = models.CASCADE , related_name="for_reply_1")
    reply_video = models.ForeignKey( detail , on_delete = models.CASCADE )

    reply_of_reply = models.ManyToManyField("self" , blank = True )
    reply_text = models.CharField( max_length = 2000  , default=" ")
    
    
    def __str__(self):
        return f"ID : {self.id} || Time : {self.reply_text} || personName : {self.person_id}"

# class LikeModelForComments(models.Model):
#     id = models.AutoField(primary_key=True , unique=True)
#     all_likes_on_comment = models.ManyToManyField( sign  , blank=False  , related_name="all_likes_on_comment" )
#     all_dislikes_on_comment =  models.ManyToManyField( sign  , blank=False ,   related_name="all_dislikes_on_comment" )

#     @property
#     def total_likes(self):
#         return self.all_likes_on_comment.all().count()

#     @property
#     def total_dislikes(self):
#         return self.all_dislikes_on_comment.all().count()


#     def __str__(self):
#         return f'ID : {str(self.id)} || VIDEO ID : {str(self.id)}'

# Comments Functionality  
class Commentss(models.Model):
    created_time = models.DateTimeField( auto_now_add = True )
    comment_text = models.CharField(max_length = 2000 , default=" ")
    user_id = models.ForeignKey( sign  , on_delete = models.CASCADE  , related_name="user_id") 
    parent = models.ForeignKey( "self" , on_delete = models.CASCADE  , blank=True  , null = True  )
    video_id = models.ForeignKey( detail , on_delete = models.CASCADE , related_name="video_id" )
    #like = models.OneToOneField( LikeModelForComments , on_delete=models.CASCADE  , blank=True)
    likes_on_comment  = models.ManyToManyField( sign  , blank=True  , related_name="likes_on_comment")
    dis_likes_on_comment = models.ManyToManyField( sign  , blank=True  )


    @property
    def total_likes_on_comment( self ):
        return self.likes_on_comment.all().count() 

    def total_dis_likes_on_comment( self ):
        return self.dis_likes_on_comment.all().count()
    

    def __str__(self):
        return f"ID : {self.id} || ime : {self.comment_text} || personName : {self.user_id}"

class LikeModel(models.Model):
    id = models.AutoField(primary_key=True , unique=True)
    video = models.OneToOneField( detail , on_delete=models.CASCADE )
    all_likes = models.ManyToManyField( sign  , blank=False)

    @property
    def total_likes(self):
        return self.all_likes.all().count()


    def __str__(self):
        return f'ID : {str(self.id)} || VIDEO ID : {str(self.video)}'


# REFERRAL MODEL
import uuid
def generate_ref_code():
    code = str(uuid.uuid4()).replace("-" , "")[:12]
    return code

class RefferalLink(models.Model):
    refferal_code = models.CharField(max_length=12  , blank=True , default="" , unique = True )
    refferal_by = models.ForeignKey(sign , on_delete=models.CASCADE , related_name='refferal_by')
    email = models.EmailField( blank=True , null = True  , max_length = 122)
    refferal_for = models.CharField(max_length=12  , blank=True , default="" )
    refferal_plateform = models.CharField(max_length=100 , blank=True)
    is_clicked = models.BooleanField(default=False)
    is_signup = models.BooleanField(default=False)
    is_creater = models.BooleanField(default=False)
    is_uploaded = models.BooleanField(default=False)
    created_time = models.DateTimeField(auto_now_add=True)
    updated_time = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'ID : {str(self.id)} || Refferal By : {str(self.refferal_by)}'

    def save(self, *args , **kwargs ) :
        if self.refferal_code == "":
            self.refferal_code = generate_ref_code()

        super().save(*args , **kwargs)










import json
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
    
#Notification
class Notification(models.Model):
    notice=models.CharField(max_length=30)
    sent=models.BooleanField(default=False)


   
    def __str__(self):
        return str(self.notice)

    def save(self,*args,**kwargs):
        channel_layer=get_channel_layer()
        notification_objs=Notification.objects.filter(sent=False).count()
        data={'count':notification_objs,'current_notification':self.notice}
        async_to_sync(channel_layer.group_send)(
            'gossip',{
                'type':'send_notification',
                'value':json.dumps(data)
            }
        )
        super(Notification,self).save(*args,**kwargs)