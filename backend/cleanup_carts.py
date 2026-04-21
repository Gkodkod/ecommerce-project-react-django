from django.contrib.auth.models import User
from store.models import Cart
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
django.setup()

def cleanup():
    for user in User.objects.all():
        carts = Cart.objects.filter(user=user)
        if carts.count() > 1:
            latest = carts.latest('created_at')
            deleted_count = carts.exclude(id=latest.id).delete()
            print(f"Cleaned up {deleted_count[0]} duplicate carts for user: {user.username}")
        else:
            print(f"No duplicates for user: {user.username}")

if __name__ == "__main__":
    cleanup()
