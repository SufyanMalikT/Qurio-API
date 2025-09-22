from rest_framework import serializers
from .models import CustomUser, Tags, Questions, Answers, Vote
from rest_framework.exceptions import ValidationError
class CustomUserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    password2 = serializers.CharField(write_only=True)
    class Meta:
        model = CustomUser 
        fields = ['id','username','email','password','password2']
        read_only_fields = ['id']

    def validate(self, attrs):
        request = self.context.get('request')
        if request.method != 'PATCH':
            if attrs['password'] != attrs['password2']:
                raise ValidationError({'password':'Passwords do not match'})
        return attrs
        
        
    def create(self, validated_data):
        validated_data.pop('password2')
        password = validated_data.pop('password')

        user = CustomUser.objects.create(**validated_data)
        user.set_password(password)

        user.save()
        return user
    
    def update(self, instance, validated_data):
        password = validated_data.pop('password',None)
        password2 = validated_data.pop('password2',None)
        for attr,value in validated_data.items():
            setattr(instance,attr,value)
        if password:
            instance.set_password(password)
        instance.save()
        return instance
    
class TagSerializer(serializers.ModelSerializer):
    questions = serializers.PrimaryKeyRelatedField(queryset=Questions.objects.all(),many=True,required=False)
    class Meta:
        model = Tags
        fields = '__all__'
        read_only_fields = ['id']


class QuestionsSerializer(serializers.ModelSerializer):
    author = CustomUserSerializer(read_only=True)
    tags = serializers.PrimaryKeyRelatedField(queryset=Tags.objects.all(),many=True)
    class Meta:
        model = Questions
        fields = ['id','title','body','author','tags','posted_at','updated_at','views','is_resolved']
        read_only_fields = ['id']

    
class AnswerSerializer(serializers.ModelSerializer):
    question = serializers.PrimaryKeyRelatedField(queryset=Questions.objects.all(),required=True)
    author = CustomUserSerializer(read_only=True)
    class Meta:
        model = Answers
        fields = ['id','body','question','author','created_at','updated_at']
        read_only_fields = ['id']


class VoteSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(queryset=CustomUser.objects.all())
    answer = serializers.PrimaryKeyRelatedField(queryset=Answers.objects.all())
    class Meta:
        model = Vote 
        fields = ['id','user','answer','value']
        read_only_fields = ['id']



