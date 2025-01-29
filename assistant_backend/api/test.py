from django.contrib.auth.models import User

# Replace 'kamil' with your actual username
try:
    user = User.objects.get(username='kamil')
    print(user)  # Should output user details
    print(user.check_password('123'))  # Should return True if the password is correct
except User.DoesNotExist:
    print("User does not exist")
