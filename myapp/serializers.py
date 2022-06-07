from dataclasses import field
from importlib.metadata import files
from re import L
from urllib import request
from xml.parsers.expat import model
from numpy import in1d
from rest_framework import serializers
from .models import * 


#profile
class signserializers(serializers.ModelSerializer):
    class Meta():
        model=sign
        fields='__all__'
        interest = serializers.MultipleChoiceField(choices=INTERESTS)
        
        
#___________________________________________________________________________________________________________________________
class supportserializers(serializers.ModelSerializer):
    class Meta:
        model=Support
        fields='__all__'
# ___________________________________________________________________________________________________________________________
#workbase serializer

    class Meta:
        model=workbaseinfo
        fields=('id','workbasename','workbasechoices','userid','wbemail','wbdescription','location','supporters')
        #depth=2

#____________________________________________________________________________________________________________________
#serializer for file detailing
class DetailGetSerializer(serializers.ModelSerializer):
   all_timeline=serializers.SerializerMethodField('timeline') 
  
   def timeline(self,obj):
       all_obj=Addresources.objects.filter(video_id=obj.id)
       return addresourceserializer(all_obj,many=True).data

   class Meta():
        model=detail
        fields=('videoid','id','title','file','description','compress','customthumbnail','tags','skills','targetaudience','agerestriction',"isCommentsOn","isLikeCountOn","isAudioCommentOn","publish",  "published_on","user_id","likesvideo",'user_id','all_timeline')
        depth=1

class DetailSerializer(serializers.ModelSerializer):
   all_timeline=serializers.SerializerMethodField('timeline') 
  
   def timeline(self,obj):
       all_obj=Addresources.objects.filter(video_id=obj.id)
       return addresourceserializer(all_obj,many=True).data

   class Meta():
        model=detail
        fields='__all__'#('videoid','id','title','file','description','compress','customthumbnail','tags','skills','targetaudience','agerestriction',"isCommentsOn","isLikeCountOn","isAudioCommentOn","publish",  "published_on","user_id","likesvideo",'user_id','all_timeline')
      


class video_view_serializer(serializers.ModelSerializer):
    class Meta:
        model=view
        fields='__all__'
        depth=1


#________________________________________________________________________________________________________________
#model for videos 

# serializers for document verification
class doc_verificationSerializer(serializers.ModelSerializer):
    user_id=signserializers()
    class Meta():
        model=doc_verification
        fields=[ 'id','user_id','firstname','lastname','email','qualification','specialized','skill_tags','year_of_experience' ]
        #depth=1

    # def update(self,instance,validated_data):
    #     userdata=validated_data.pop('user_id')
    #     userserializer=signserializers()
    #     super(self.__class__,self).update(instance,validated_data)
    #     super(signserializers,userserializer).update(instance.user_id,userdata)
    #     return instance
#_____________________________________________________________________________________________________________________________
#connect serializer
class connectSerializer(serializers.ModelSerializer):
    class Meta():
        model=connect
        fields=['id','user','connect','title','tags','published_on','likes','number_of_likes']
    
    # def get_liked_by_req_user(self, obj):
    #     user = self.context['request'].user
    #     return user in obj.likes.all()

class connect_comment_serializer(serializers.ModelSerializer):
    reply=serializers.SerializerMethodField('child_comment')
    def child_comment(self,obj):
            all_obj=connect_comment.objects.filter(parent=obj.id)
            return connect_comment_serializer(all_obj,many=True).data

    class Meta():
        model=connect_comment
        fields=['id','commentid','user','post_comment','post_created_on','post','parent','likes_comment','comment_dislikes','reply','like_active','dislike_active']
#______________________________________________________________________________________________________________________________
    

#about_serializer
class tag(serializers.ModelSerializer):
    class Meta():
        model=section
        fields='__all__'
#_________________________________________________________________________________________________________________________

class playlist_videoserializer(serializers.ModelSerializer):
    class Meta:                    # so you have to mention same field name that you had used in model for nested serializer
        model=playlist
        fields='__all__'
        depth=1

#for playlist serializer
class playlist_post_videoserializer(serializers.ModelSerializer):
   # files=DetailSerializer(many=True) # whenever we will use Nested Serializer  
    class Meta:                    # so you have to mention same field name that you had used in model for nested serializer
        model=playlist
        fields='__all__'
        filter_fields = ('files__id',)

#for group serializer

from django.http import JsonResponse
from django.shortcuts import HttpResponse
from django.forms.models import model_to_dict
class ListsFieldForGroupSerializer(serializers.RelatedField):
    def to_representation(self, value):
        data = {"id" : value.id , "grouplistid": value.grouplistid , "name" : value.name  , "group_list_image": value.group_list_image.url  } 
        return data   # f"{value.files.all().values('id' , 'videoid' )}" 

class groupserializer(serializers.ModelSerializer):
    #lists=playlist_videoserializer(read_only=True) 
    #lists = serializers.StringRelatedField(many=True)       #This will return Model __str__ functioN
    lists  =  ListsFieldForGroupSerializer( many = True , read_only=True )
    class Meta:                                 #It is used when you have to embeded one serializer in other serializer
        model=group
        fields=[ 'id','groupskillid','userid','title','lists' ]
        #depth = 1

class group_post_serializer(serializers.ModelSerializer):
    #list=playlist_videoserializer() 
       #here we have nested serializer.
    class Meta:                                 #It is used when you have to embeded one serializer in other serializer
        model=group
        fields=['id','groupskillid','userid','title','list']

#___________________________________________________________________________________________________________________________

#serializer for report
class reportserializer(serializers.ModelSerializer):

    class Meta:
        model=report4
        fields=('id' , 'reportid' , 'report_user' , 'report_file' , 'report_post' , 'report_descript' , 'choice'  , 'created_at' ) #'__all__'
#________________________________________________________________________________________________________________________
class question1serializer(serializers.ModelSerializer):
    class Meta:
        model=question
        fields=['id','imgfile','ques','question','answer','isrequired']
        #depth=1

class question2serializer(serializers.ModelSerializer):
    class Meta:
        model=question2
        fields=['id','imgfile','question','answer','isrequired','questionnaire']
        read_only_fields=('questionnaire',)
        #depth=1

class question3serializer(serializers.ModelSerializer):
    class Meta:
        model=question3
        fields=['id','questionnaire','question','imgfile','option1','option2','option3','option4','img1_option','img2_option','img3_option','img4_option','answer','isrequired']
        read_only_fields=('isrequired',)
        #depth=1
#____________________________________________________________________________________________________________________________________________


    def question_qna_function(self,obj):
        all_obj=question2.objects.filter(questionnaire=obj.ques_id)
        return question2serializer(all_obj,many=True).data

    def question_mcq_function(self,obj):
        all_obj=question3.objects.filter(questionnaire=obj.ques_id)
        return question3serializer(all_obj,many=True).data
    class Meta:
        model=questionnaires
        fields=['ques_id','questionnaireid','userid','videoid','description','question_text','question_qna','question_mcq']
        #depth=1

class questionnairepostserializer(serializers.ModelSerializer):
    class Meta:
        model=questionnaires
        fields=['ques_id','questionnaireid','userid','videoid','description']
    

#_________________________________________________________________________________________________________________

class addresourceserializer(serializers.ModelSerializer):
    support=serializers.SerializerMethodField('supporttimeline')

    def supporttimeline(self,obj):
        all_obj=supportTimeline.objects.select_related( 'resources' , 'videorefernce' ).filter(resources=obj.id)
        if all_obj :
             return supportTimelineserializer(all_obj,many=True).data
        return None
    class Meta:    
        model=Addresources
        fields=['id','user_id','video_id','timeline','resourcesfile','questionnaire','support'] #here we have used other serializer method 
        #depth=1

class addresources_post_serializer(serializers.ModelSerializer):
     class Meta:    
        model=Addresources
        fields=('id','user_id','video_id','timeline','resourcesfile','questionnaire')


from django.forms.models import model_to_dict
class supportTimelineserializer(serializers.ModelSerializer):
    class Meta:
        model=supportTimeline
        fields=['id','hours','minutes','seconds','resources','videorefernce']
        
              
class supportgetTimelineserializer(serializers.ModelSerializer):
    class Meta:
        model=supportTimeline
        fields=['id','hours','minutes','seconds','resources','videorefernce']
        depth=1
        
    
    
   

#___________________________________________________________________________________________________________________

class ContactSerializerModel(serializers.ModelSerializer):
    class Meta:
        model = Contact
        fields = ['id','name','gmail', 'status','auth_token']


class Emailverificationserializer(serializers.ModelSerializer):
    token=serializers.CharField(max_length=555)
    class Meta:
        model=Contact
        fields=['token']

class UserSerializer(serializers.ModelSerializer):
    contact_id = ContactSerializerModel()
    #skills = serializers.ListField(child=serializers.ListField())

    class Meta:
        model = abc
        fields = [
            'id',
          'username',
          'password',
          'skills',
          'contact_id',
         
         
        ]
    

    def create(self, validated_data):
        contact_data = validated_data.pop('contact_id')  
        contact = Contact.objects.create(**contact_data)
        user = abc.objects.create(contact_id=contact, **validated_data)
        return user

    def update(self, instance, validated_data):
        user_data = validated_data.pop('contact_id')
        user_serializer = ContactSerializerModel()
        super(self.__class__, self).update(instance,validated_data)
        super(ContactSerializerModel,user_serializer).update(instance.contact_id,user_data)
        return instance

    

#_______________________________________________________________________________________________________________
#workbase(display,branding)
class basic_display_serializer(serializers.ModelSerializer):
    class Meta:
        model=basic_display
        fields=['id','highlight1','highlight2','highlight3','highlight4','highlight5']
       

class display_serializer(serializers.ModelSerializer):
    class Meta:
        model=basic_display
        fields=['id','highlight1','highlight2','highlight3','highlight4','highlight5']
        depth=1
       
    
   
class basic_branding_serializer(serializers.ModelSerializer):
    class Meta:
        model=basic_branding
        fields='__all__'
        
#_____________________________________________________________________________________________________________________________
class fileserializer(serializers.ModelSerializer):

    class Meta:
        model=MyModel
        fields='__all__'

#____________________________________________________________________________________________________________________
class monitizeserializer(serializers.ModelSerializer):
    class Meta:
        model=sharemon
        fields='__all__'

#_____________________________________________________________________________________________________________________



















#__________________________________________________________



# class ReplySerializer(serializers.ModelSerializer):
#     class Meta:
#         model =  Reply
#         fields = "__all__"
        



# class CommentDetailSerializer ( serializers.ModelSerializer ):
#     #user_name = serializers.CharField( source="user_id.name" ,  read_only=True )
#      class Meta:
#         model=detail
#         fields= ['videoid']




class EagerLoadingMixin:
    @classmethod
    def setup_eager_loading(cls, queryset):
        if hasattr(cls, "_SELECT_RELATED_FIELDS"):
            queryset = queryset.select_related(*cls._SELECT_RELATED_FIELDS)
        if hasattr(cls, "_PREFETCH_RELATED_FIELDS"):
            queryset = queryset.prefetch_related(*cls._PREFETCH_RELATED_FIELDS)
        return queryset 
        


# TODO: in this API WE NEED TO Remove method fields
class CommentSerializer( EagerLoadingMixin , serializers.ModelSerializer ):
    #user_name = serializers.CharField( source="user_id.name" ,  read_only=True )
    profile = serializers.CharField( source="user_id.profilePic.url" ,  read_only=True )
    # video_id = CommentDetailSerializer(read_only=True)
    

    class Meta:
        model = Commentss
        fields = ['id' , 'profile' , "parent" ,  "video_id" ,  "likes_on_comment" , "dis_likes_on_comment" , 
        "comment_text" ,   "user_id" , 'like_active' , 'dislike_active'  , 'created_at'  ] 
    
    _SELECT_RELATED_FIELDS = ['user_id' , 'video_id__user_id']
    _PREFETCH_RELATED_FIELDS = ['likes_on_comment' , 'dis_likes_on_comment']




class CommentSerializer_single_instance(serializers.ModelSerializer ):
    
    is_creater  =  serializers.SerializerMethodField( source="get_is_creater" ,  read_only=True )
    profile = serializers.CharField( source="user_id.profilePic.url" ,  read_only=True )


    def get_is_creater(self , obj , *args  , **kwargs ): 
        try:
            creater_obj = sign.objects.get( id = str(obj.video_id.user_id.id ) )
            comment_user_obj = sign.objects.get( id = obj.user_id.id )
            if creater_obj.id == comment_user_obj.id:
                return True 
            return False
        except:
            return None
            
   
    class Meta:
        model = Commentss
        fields = ['id' , 'profile' , "parent" ,  "is_creater" ,  "video_id" ,  "likes_on_comment" , "dis_likes_on_comment" , 
        "comment_text" ,   "user_id" , 'like_active' , 'dislike_active'  , 'created_at'  ] 




# TODO: in this API WE NEED TO Remove method fields
class questionnaireserializer( EagerLoadingMixin , serializers.ModelSerializer):
    question_text=serializers.SerializerMethodField('quest_text_function')
    question_qna=serializers.SerializerMethodField('question_qna_function')
    question_mcq=serializers.SerializerMethodField('question_mcq_function')
    '''
    THIS SerializerMethodField FIELD INCREASE 3 QUERY PER OBJECTS
    '''

    def quest_text_function(self,obj):
        all_obj=question.objects.filter(ques=obj.ques_id)
        return question1serializer(all_obj,many=True).data

    def question_qna_function(self,obj):
        all_obj=question2.objects.filter(questionnaire=obj.ques_id)
        return question2serializer(all_obj,many=True).data

    def question_mcq_function(self,obj):
        all_obj=question3.objects.filter(questionnaire=obj.ques_id)
        return question3serializer(all_obj,many=True).data
    class Meta:
        model=questionnaires
        fields=['ques_id','questionnaireid','userid','videoid','description','question_text','question_qna','question_mcq']
        depth=1    # IF REMOVE DEPTH THEN 1 QUERY PER OBJECTS REDUSE
    

    _SELECT_RELATED_FIELDS = ['userid' , 'videoid']
    

class workserializer(serializers.ModelSerializer):
    supporters=serializers.SerializerMethodField('support_function')
    def support_function(self,obj):
        all_obj=Support.objects.filter(wbname=obj.id)  
        return supportserializers(all_obj,many=True).data

    class Meta:
        model=workbaseinfo
        fields=('id','workbasename','workbasechoices','userid','wbemail','wbdescription','location','supporters')



class timelineSerializer(serializers.ModelSerializer):
    class Meta:
        model = timelineModel
        fields = "__all__"


class RefferalLinkSerializer(serializers.ModelSerializer):
    class Meta:
        model = RefferalLink
        fields = ['id' ,   'refferal_code' , 'refferal_by' , 'refferal_for' , 'email' , 'refferal_plateform'  , 'is_clicked' , 'is_signup' , 'is_creator' , 'is_uploaded' , 'created_time' , 'updated_time' ]



class LikeModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = LikeModel
        fields = "__all__"

class ReplySerializer(serializers.ModelSerializer):
    class Meta:
        model =  Reply
        fields = "__all__"


class courseserializer(serializers.ModelSerializer):
    class Meta:
        model=mycourse
        fields='__all__'





class User_Historyserializer(serializers.ModelSerializer):
    class Meta:
        model=User_History
        fields='__all__'