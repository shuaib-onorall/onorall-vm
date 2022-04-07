from distutils.command.upload import upload
from enum import unique
from ipaddress import ip_address
from tabnanny import verbose
from unittest.mock import DEFAULT
from django.db import models
from django.contrib.auth.models import User
from django.forms import CharField
from django.urls import reverse
from django.contrib.auth.models import User
import uuid
from django.contrib.contenttypes.fields import GenericForeignKey
#from django_clamd.validators import validate_file_infection  #-----------this is used to detect the malware detection

import random, string

def random_id_field():
  rnd_id = ''.join(random.choices(string.ascii_letters + string.digits, k=12))
  return rnd_id

def random_profile():
    random_list = ['profilePic\img2.png ' ,
     'profilePic\img4.jpg' ,
     'profilePic\img7.jpg' ]
    random_path = random.choices(random_list)[0]
    return random_path



#_______________________________________________________________________________________________________________________
#user model
class sign(models.Model):
    id = models.CharField(max_length=12, unique=True, primary_key=True,  default=random_id_field)
    name=models.CharField(max_length=30)
    phone=models.CharField(max_length=13,null=True,blank=True)
    gmail=models.EmailField(null=True,blank=True)
    iscreator=models.BooleanField(default=False)
    signup_referral_by=models.IntegerField(default=0)
   
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
    return 'http://192.168.1.85:8000/general/' +(videoid) #this is used of custom url


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

    

    def __str__(self) -> str:
        return  str(self.file) 

    @property
    def total_likes(self):
        return self.likesvideo.all().count()


class view(models.Model):
    video=models.OneToOneField(detail,related_name='count',on_delete=models.CASCADE)
    ip_address=models.CharField(max_length=50)
    session=models.CharField(max_length=50)
    view=models.PositiveIntegerField(default=0)

    def __str__(self):
        return f'ip_address:{str(self.ip_address)} '

#_______________________________________________
class timelineModel(models.Model):
    time = models.CharField(max_length=200)
    user_id=models.ForeignKey(sign,null=True,blank=True,on_delete=models.CASCADE)
    resourcesid = models.CharField(max_length=12, unique=True,   default=random_id_field)
    resourcesfile=models.FileField(upload_to='resources/',null=True,blank=True)
    connected_to = models.ForeignKey(detail , on_delete=models.CASCADE)
    
    def __str__(self) -> str:
        return  str(self.id)


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
from django.dispatch import receiver
from django.db.models.signals import post_save,pre_delete

#community post comment
class connect_comment(models.Model):
    commentid = models.CharField(max_length=12, unique=True,   default=random_id_field)
    user=models.ForeignKey(sign,blank=True,on_delete=models.CASCADE)
    post_comment=models.TextField()
    post_created_on=models.DateTimeField(auto_now=True)
    post=models.ForeignKey(connect,blank=True,on_delete=models.CASCADE)
    parent=models.ForeignKey('connect_comment',null=True,blank=True,related_name='replies',on_delete=models.CASCADE)
    likes_comment=models.ManyToManyField(sign,blank=True ,related_name='Post_comment_likes')
    comment_dislikes=models.ManyToManyField(sign,blank=True,related_name='Post_comment_dislkikes')
    like_active=models.CharField(max_length=12,blank=True,null=True)
    dislike_active=models.CharField(max_length=12,blank=True,null=True)

    class Meta:
        ordering=['-post_created_on']
   
    def __str__(self) -> str:
        return f'{self.user}||{self.parent}'
       
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
    group_list_image=models.ImageField(upload_to='grouplist/',null=True,blank=True,verbose_name='group_list_image')
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
import json
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
    
#Notification
class Notification(models.Model):
    notice=models.TextField()
    sent=models.BooleanField(default=False)
   
    def __str__(self):
        return str(self.notice)

    #def save(self,*args,**kwargs):
        #channel_layer=get_channel_layer()
        #data={'current':self.notice} ------->>>>>>>> this is override the save method 
        #async_to_sync(channel_layer.group_send)(
            #'gossip',{
                #'type':'send_notification',
                #'value':json.dumps(data)
            #}
        #)
        #super(Notification,self).save(*args,**kwargs)

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
    created_at=models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints=[models.UniqueConstraint(fields=['report_file','report_user'],name='report_user_file'),
                    models.UniqueConstraint(fields=['report_post','report_user'],name='report_user_post')
                    ]

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
    user_id=models.ForeignKey(sign,on_delete=models.CASCADE)
    resourcesid = models.CharField(max_length=12, unique=True,   default=random_id_field)
    video_id=models.ForeignKey(detail,on_delete=models.CASCADE)
    timeline=models.CharField("hr:min:se",max_length=20)
    resourcesfile=models.FileField(upload_to='resources/',null=True,blank=True)
    questionnaire=models.ForeignKey(questionnaires,related_name='questionnaire',null=True,blank=True,on_delete=models.CASCADE)

    def __str__(self) -> str:
        return str(self.user_id)

class supportTimeline(models.Model):
    resources=models.ForeignKey(Addresources,null=True,blank=True,on_delete=models.CASCADE)
    hours=models.PositiveIntegerField()
    minutes=models.PositiveIntegerField()
    seconds=models.PositiveIntegerField()
    #toend=models.CharField(max_length=40)
    videorefernce=models.ForeignKey(detail,null=True,blank=True,on_delete=models.CASCADE)

    def __str__(self):
        return str(self.resources)





    

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
# REFERRAL MODEL
import uuid
def generate_ref_code():
    code = str(uuid.uuid4()).replace("-" , "").replace("/" , "-")[:12]
    return code

class RefferalLink(models.Model):
    refferal_code = models.CharField(max_length=12  , blank=True , default="" , unique = True )
    refferal_by = models.ForeignKey(sign , on_delete=models.CASCADE , related_name='refferal_by')
    email = models.EmailField( blank=True , null = True  , max_length = 122)
    refferal_for = models.CharField(max_length=12  , blank=True , default="" )
    refferal_plateform = models.CharField(max_length=100 , blank=True)
    is_clicked = models.BooleanField(default=False)
    is_signup = models.BooleanField(default=False)
    is_creator = models.BooleanField(default=False)
    is_uploaded = models.BooleanField(default=False)
    created_time = models.DateTimeField(auto_now_add=True)
    updated_time = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'ID : {str(self.id)} || Refferal By : {str(self.refferal_by)}'

    def save(self, *args , **kwargs ) :
        if self.refferal_code == "":
            self.refferal_code = generate_ref_code()
        super().save(*args , **kwargs)








#_____________________comments

class Commentss(models.Model):
    created_time = models.DateTimeField( auto_now_add = True )
    comment_text = models.CharField(max_length = 2000 , default=" ")
    user_id = models.ForeignKey( sign  , on_delete = models.CASCADE  , related_name="user_id") 
    parent = models.ForeignKey( "self" , on_delete = models.CASCADE  , blank=True  , null = True  )
    video_id = models.ForeignKey( detail , on_delete = models.CASCADE , related_name="video_id" )
    #like = models.OneToOneField( LikeModelForComments , on_delete=models.CASCADE  , blank=True)
    likes_on_comment  = models.ManyToManyField( sign  , blank=True  , related_name="likes_on_comment")
    dis_likes_on_comment = models.ManyToManyField( sign  , blank=True  )

    like_active = models.CharField(max_length = 2000 , blank=True , default='null')
    dislike_active = models.CharField(max_length = 2000 , blank=True  , default = 'null' )
    


    @property
    def total_likes_on_comment( self ):
        return self.likes_on_comment.all().count() 

    def total_dis_likes_on_comment( self ):
        return self.dis_likes_on_comment.all().count()
    

    def __str__(self):
        return f"ID : {self.id} || ime : {self.comment_text} || personName : {self.user_id}"
    
