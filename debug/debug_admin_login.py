import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'play_pal_project.settings')
django.setup()

from django.contrib.auth import authenticate
from accounts.models import CustomUser

# Test the exact authentication Django admin uses
email = 'super@gmail.com'  # your superuser email
password = '21272829Ab*dmy'   # your superuser password

print("=== Testing Admin Authentication ===")

# Method 1: Using authenticate (what admin uses)
user = authenticate(email=email, password=password)
print(f"Authenticate result: {user}")
if user:
    print(f"User: {user.email}")
    print(f"Is superuser: {user.is_superuser}")
    print(f"Is staff: {user.is_staff}")
    print(f"Is active: {user.is_active}")

# Method 2: Direct database check
print("\n=== Direct Database Check ===")
try:
    db_user = CustomUser.objects.get(email=email)
    print(f"User exists: {db_user.email}")
    print(f"DB - Is superuser: {db_user.is_superuser}")
    print(f"DB - Is staff: {db_user.is_staff}")
    print(f"DB - Is active: {db_user.is_active}")
    print(f"Password check: {db_user.check_password(password)}")
except CustomUser.DoesNotExist:
    print("User not found in database")
