from django.db import models

class Note(models.Model):
    
    CATEGORY = (('BUSINESS', 'Business'),
                ('PERSONAL', 'Personal'),
                ('IMPORTANT', 'Important'))
    
    
    title = models.CharField(max_length=100)
    body = models.TextField()
    slug = models.SlugField(unique=True)
    category = models.CharField(max_length=15, choices=CATEGORY, default="PERSONAL")
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
