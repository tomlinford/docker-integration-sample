from django.contrib.auth.models import User

User.objects.create_user(username="test1", password="password12")
User.objects.create_user(username="test2", password="password12")
