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
