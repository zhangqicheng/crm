from django.test import TestCase
# Create your tests here.
import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "crm.settings")
import django
django.setup()
from app01 import models
#<class 'app01.models.Enrollment'>


