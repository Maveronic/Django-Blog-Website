from django.contrib import admin
from blog.models import Post

# Makes the Post model visible in the Admin panel
admin.site.register(Post)
