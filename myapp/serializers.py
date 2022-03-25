from dataclasses import field
from re import L
from urllib import request
from xml.parsers.expat import model
from rest_framework import serializers
from .models import * 


#profile
class signserializers(serializers.ModelSerializer):
    class Meta():
        model=sign
        fields=['id','name','gmail','phone','iscreator']
#___________________________________________________________________________________________________________________________
class supportserializers(serializers.ModelSerializer):
    class Meta:
        model=Support
        fields='__all__'
# ___________________________________________________________________________________________________________________________
#workbase serializer
class workserializer(serializers.ModelSerializer):
    supporters=serializers.SerializerMethodField('support_function')
    def support_function(self,obj):
        all_obj=Support.objects.filter(wbname=obj.id)  
        return supportserializers(all_obj,many=True).data

    class Meta:
        model=workbaseinfo
        fields=('id','workbasename','workbasechoices','userid','wbemail','wbdescription','location','supporters')
        depth=2

#____________________________________________________________________________________________________________________
#serializer for file detailing
class DetailSerializer(serializers.ModelSerializer):
   all_timeline=serializers.SerializerMethodField('timeline')
   def timeline(self,obj):
       all_obj=Addresources.objects.filter(video_id=obj.id)
       l=[]
       for i in all_obj:
           l.append(i.id)
       return l

   class Meta():
        model=detail
        fields=('videoid','id','title','file','description','customthumbnail','tags','skills','targetaudience','agerestriction',"isCommentsOn","isLikeCountOn","isAudioCommentOn","publish",  "published_on","user_id","likesvideo",'user_id','all_timeline')
        depth=1

#________________________________________________________________________________________________________________
#model for videos 

# serializers for document verification
class doc_verificationSerializer(serializers.ModelSerializer):
    user_id=signserializers()
    class Meta():
        model=doc_verification
        fields=['id','user_id','firstname','lastname','email','qualification','specialized','skill_tags','year_of_experience','user_id']
        depth=5

    def update(self,instance,validated_data):
        userdata=validated_data.pop('user_id')
        userserializer=signserializers()
        super(self.__class__,self).update(instance,validated_data)
        super(signserializers,userserializer).update(instance.user_id,userdata)
        return instance

#_____________________________________________________________________________________________________________________________

#connect serializer
class connectSerializer(serializers.ModelSerializer):
    class Meta():
        model=connect
        fields=['id','user','connect','title','tags','published_on','likes','number_of_likes']
    
    def get_liked_by_req_user(self, obj):
        user = self.context['request'].user
        return user in obj.likes.all()
#______________________________________________________________________________________________________________________________
    

#about_serializer
class tag(serializers.ModelSerializer):
    class Meta():
        model=section
        fields='__all__'


#_________________________________________________________________________________________________________________________

#for playlist serializer
class playlist_videoserializer(serializers.ModelSerializer):
    files=DetailSerializer(many=True) # whenever we will use Nested Serializer  
    class Meta:                    # so you have to mention same field name that you had used in model for nested serializer
        model=playlist
        fields='__all__'
        filter_fields = ('files__id',)

#for group serializer

class groupserializer(serializers.ModelSerializer):
    list=playlist_videoserializer(many=True)    #here we have nested serializer.
    class Meta:                                 #It is used when you have to embeded one serializer in other serializer
        model=group
        fields='__all__'

def create(self,**validated_data):
    groupdata=validated_data.pop('list')
    data=playlist.objects.create(**groupdata)
    groupvideo=group.objects.create(list=data,**validated_data)
    return groupvideo

def update(self,instance,validated_data):
    groupdata=validated_data.pop(list)
    serilaizer=groupserializer()
    super(self.__class__,self).update(instance,validated_data)
    super(groupserializer,serilaizer).update(instance.list,groupdata)

#_______________________________________________________________________________________________________________________

#comment serializer
class CommentChildSerializer(serializers.ModelSerializer):
    parent_id = serializers.PrimaryKeyRelatedField(queryset=Comment.objects.all(),source='parent.id')
    class Meta:
        model = connect_comment
        fields = ( 'post_comment', 'id','parent_id')


    def create(self, validated_data):
        subject = connect_comment.objects.create(parent=validated_data['parent']['id'], content=validated_data['postcomment'])

class CommentSerializer(serializers.ModelSerializer):
    reply_count = serializers.SerializerMethodField()
    replies = serializers.SerializerMethodField()
    class Meta:
        model = connect_comment
        fields = ('id','post_comment','user','post', 'parent', 'reply_count', 'replies','likes')
        # depth = 1

    def get_reply_count(self, obj):
        if obj.is_parent:
            return obj.children().count()
        return 0


    def get_replies(self, obj):
        if obj.is_parent:
            return CommentChildSerializer(obj.children(), many=True).data
        return None
#___________________________________________________________________________________________________________________________

#serializer for report
class reportserializer(serializers.ModelSerializer):
    class Meta:
        model=report4
        fields='__all__'
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
        depth=1

class question3serializer(serializers.ModelSerializer):
    class Meta:
        model=question3
        fields=['id','questionnaire','question','imgfile','option1','option2','option3','option4','img1_option','img2_option','img3_option','img4_option','answer','isrequired']
        read_only_fields=('isrequired',)
        depth=1
#____________________________________________________________________________________________________________________________________________

class questionnaireserializer(serializers.ModelSerializer):
    question_text=serializers.SerializerMethodField('quest_text_function')
    question_qna=serializers.SerializerMethodField('question_qna_function')
    question_mcq=serializers.SerializerMethodField('question_mcq_function')
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
        depth=1
    

#_________________________________________________________________________________________________________________

class addresourceserializer(serializers.ModelSerializer):
    class Meta:    
        model=Addresources
        fields=['id','user_id','video_id','timeline','resourcesfile','questionnaire'] #here we have used other nested serializer method 
        read_only_fields=('questionnaire',)
        depth=1   
#___________________________________________________________________________________________________________________

class ContactSerializerModel(serializers.ModelSerializer):
    class Meta:
        model = Contact
        fields = ['name', 'status']

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
      
    def get_contact_id(self, post):
        return abc.contact_id.values_list('contact_id', flat=True)

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

    
#for the purpose of testing 
#_______________________________________________________________________________________________________________
#workbase(display,branding)
class basic_display_serializer(serializers.ModelSerializer):
    #highlight1=DetailSerializer()
    class Meta:
        model=basic_display
        fields=['id','highlight1','highlight2','highlight3','highlight4','highlight5']
        depth = 1
    # def create(self, validated_data):
    #     print('workinggggggggggggggggggggggggggggggg')
    #     self.Meta.depth = 0
    #     instance = self.Meta.model(**validated_data)
    #     instance.save()
    #     return instance
    #     #super().create(validated_data)
        
     


        
           
        


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



class ReplySerializer(serializers.ModelSerializer):
    class Meta:
        model =  Reply
        fields = "__all__"
        
        

class CommentSerializer(serializers.ModelSerializer):

    user_name = serializers.SerializerMethodField('user_name_func')
    is_creater  =  serializers.SerializerMethodField('is_creater_func')

    # reply = serializers.SerializerMethodField('reply_func')
    # def reply_func(self , obj):
    #     all_obj = Commentss.objects.filter(parent = obj.id)
    #     return CommentSerializer(all_obj , many=True ).data
    
    def user_name_func(self,obj):
        obj=sign.objects.get(id = obj.user_id.id)
        return obj.name

    def is_creater_func(self , obj):
        creater_obj = sign.objects.get(id = obj.video_id.user_id.id)
        comment_user_obj = sign.objects.get(id = obj.user_id)
        if creater_obj.id == comment_user_obj.id:
            return True
        return False



    class Meta:
        model = Commentss
        fields = ['id'  , "comment_text" , "user_id"  , "parent" , "video_id"   ,  "likes_on_comment" , "dis_likes_on_comment" ,  'created_time' , 'user_name'  , 'is_creater'] #__all__"
        # depth = 1


class timelineSerializer(serializers.ModelSerializer):
    class Meta:
        model = timelineModel
        fields = "__all__"


class LikeModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = LikeModel
        fields = "__all__"


class RefferalLinkSerializer(serializers.ModelSerializer):
    class Meta:
        model = RefferalLink
        fields = ['id' , 'time' , 'refferal_code' , 'refferal_by' , 'refferal_for' , 'refferal_plateform'  , 'is_clicked' , 'is_signup' , 'is_creater' , 'is_uploaded']
