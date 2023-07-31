from django.test import TestCase
from decouple import config

test = config("DB_HOST")

# Create your tests here.
