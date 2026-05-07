import os
import django
from django.test import Client
from django.urls import reverse

import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.append(str(BASE_DIR))

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'cafe.settings')
django.setup()

def test_staff_login():
    client = Client()
    login_url = reverse('login')
    
    # Try logging in as john_staff
    response = client.post(login_url, {'uname': 'john_staff', 'pword': 'staff123'})
    
    print(f"Status Code: {response.status_code}")
    print(f"Redirect URL: {response.get('Location')}")
    print(f"Session Keys: {list(client.session.keys())}")
    
    if response.status_code == 302 and response.get('Location') == reverse('staff_dashboard'):
        print("Staff login SUCCESSFUL")
    else:
        print("Staff login FAILED")

if __name__ == "__main__":
    test_staff_login()
