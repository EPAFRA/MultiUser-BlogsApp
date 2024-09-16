
from django.db import models
from django.contrib.auth.models import User
from PIL import Image
from cloudinary.models import CloudinaryField


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = CloudinaryField(
        'image', 
        blank=True, 
        null=True, 
        default='https://res.cloudinary.com/dqvewferm/image/upload/v1726457813/default_fqcgdm.jpg'
    )
    gender = models.CharField(max_length=10, choices=(('Male', 'Male'), ('Female', 'Female')), default='Male')

    def __str__(self):
        return f'{self.user.username} Profile'
    
    @property
    def get_profile_image_url(self):
        if self.image:  # Check if there's an image associated with the profile
            return self.image.url
        return 'https://res.cloudinary.com/dqvewferm/image/upload/v1726457813/default_fqcgdm.jpg'

    def save(self, *args, **kwargs):
      super(Profile, self).save(*args, **kwargs)

        
        # img = Image.open(self.image.path)

        # if img.height > 300 or img.width > 300:
        #     output_size = (300, 300)
        #     img.thumbnail(output_size)
        #     img.save(self.image.path)
