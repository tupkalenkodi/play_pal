import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'play_pal_project.settings')
django.setup()

from accounts.models import CustomUser

# Check if superuser exists
try:
    user = CustomUser.objects.filter(is_superuser=True).first()
    if user:
        print(f"Superuser found: {user.email}")
        print(f"Is superuser: {user.is_superuser}")
        print(f"Is staff: {user.is_staff}")
        print(f"Is active: {user.is_active}")
        print(f"Password hash: {user.password}")
        print(f"Salt: {user.salt}")

        # Test password manually
        test_password = input("Enter password to test: ")
        print(f"Password check: {user.check_password(test_password)}")
    else:
        print("No superuser found")
except Exception as e:
    print(f"Error: {e}")
