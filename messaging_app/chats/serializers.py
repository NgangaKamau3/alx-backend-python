from .models import User, Conversation, Message
from rest_framework import serializers
from django.contrib.auth import authenticate

class UserSerializer(serializers.ModelSerializer):
	password = serializers.CharField(write_only=True, required=True, style={'input_type': 'password'})
	
	class Meta:
		model = User
		fields = ['user_id', 'username', 'email', 'password', 'first_name', 'last_name', 'phone_number', 'date_joined']
		extra_kwargs = {
			'password': {'write_only': True},
			'user_id': {'read_only': True},
			'date_joined': {'read_only': True}
		}
		
	def create(self, validated_data):
		return User.objects.create_user(
			username=validated_data['username'],
			email=validated_data['email'],
			password=validated_data['password'],
			first_name=validated_data.get('first_name', ''),
			last_name=validated_data.get('last_name', ''),
			phone_number=validated_data.get('phone_number', '')
		)
class LoginSerializer(serializers.Serializer):
	email = serializers.EmailField()
	password = serializers.CharField()

	def validate(self, data):
		user = authenticate(**data)
		if user and user.is_active:
			return user
		raise serializers.ValidationError("Invalid Credentials")

class MessageSerializer(serializers.ModelSerializer):
	sender = UserSerializer(read_only=True)
	
	class Meta:
		model = Message
		fields = ['message_id', 'message_body', 'sent_at', 'sender']
	
	def validate_message_body(self, value):
		if not value.strip():
			raise serializers.ValidationError("Message body cannot be empty.")
		return value

class ConversationSerializer(serializers.ModelSerializer):
	participants = UserSerializer(many=True, read_only=True)
	messages = MessageSerializer(source='conversations', many=True, read_only=True)
	
	class Meta:
		model = Conversation
		fields = ['conversation_id', 'name', 'participants', 'messages', 'created_at']