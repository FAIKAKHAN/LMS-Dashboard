from django.db import models
from django.contrib.auth.models import User

class Category(models.Model):
    name = models.CharField(max_length=100)
    icon_class = models.CharField(max_length=50, help_text="FontAwesome class e.g. 'fas fa-code'")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Categories"

    class Meta:
        verbose_name_plural = "Categories"

class Profile(models.Model):
    items = [
        ('Student', 'Student'),
        ('Teacher', 'Teacher'),
    ]
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    role = models.CharField(max_length=10, choices=items, default='Student')
    profession = models.CharField(max_length=100, default="Student") # For display like "Developer", "Designer"
    profile_pic = models.ImageField(upload_to='profiles/', default='images/pic-1.jpg')

    def __str__(self):
        return self.user.username

class Course(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    tutor = models.ForeignKey(Profile, on_delete=models.CASCADE, limit_choices_to={'role': 'Teacher'})
    thumbnail = models.ImageField(upload_to='thumbnails/')
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    date_created = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.title

class Lesson(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='lessons')
    title = models.CharField(max_length=200)
    video_file = models.FileField(upload_to='videos/', blank=True, null=True)
    thumbnail = models.ImageField(upload_to='lessons/')
    description = models.TextField(blank=True)
    position = models.PositiveIntegerField(default=1)

    def __str__(self):
        return self.title
    
    class Meta:
        ordering = ['position']

class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, related_name='comments')
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comment by {self.user.username} on {self.lesson.title}"

class Contact(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=20, blank=True)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Message from {self.name}"
