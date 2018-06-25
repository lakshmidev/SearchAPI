from rest_framework import serializers

from searchapp.models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username', 
        	'email', 'date_joined')
