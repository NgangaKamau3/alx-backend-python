from .models import User, Conversation, Message
from rest_framework import serializers
from django.contrib.auth import authenticate

class Userserializer(serializers.ModelSerializer):
	password = serializers.CharField(write_only=True, required=True, style={'input_type': 'password'})
	class Meta():
		model = User
		fields = ['id', 'username', 'email', 'password', 'first_name', 'last_name', 'phone_number', 'date_joined']
		extra_kwargs = {'password': {'write_only': True},
				  'user_id': {'read_only': True},
				  'date_joined': {'read_only': True}}
		
	def create(self, validated_data):
		user = User.objects.create_user(
			username = validated_data['username'],
			email = validated_data['email'],
			password = validated_data['password'],
			first_name = validated_data['first_name', ''],
			last_name = validated_data['last_name', ''],
			phone_number = validated_data['phone_number', '']
		)
		return user
class LoginSerializer(serializers.Serializer):
	email = serializers.EmailField()
	password = serializers.CharField()

	def validate(self, data):
		user = authenticate(**data)
		if user and user.is_active:
			return user
		raise serializers.ValidationError("Invalid Credentials")

class ConversationSerializer(serializers.ModelSerializer):
	participants = Userserializer(many=True, read_only=True)
	
	class Meta:
		model = Conversation
		fields = ['conversation_id', 'name', 'participants', 'created_at']

class MessageSerializer(serializers.ModelSerializer):
	sender = Userserializer(read_only=True)
	
	class Meta:
		model = Message
		fields = ['message_id', 'message_body', 'sent_at', 'sender', 'conversation']
		extra_kwargs = {'conversation': {'write_only': True}}
	
	def validate_message_body(self, value):
		if not value.strip():
			raise serializers.ValidationError("Message body cannot be empty.")
		return value