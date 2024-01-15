from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone



class Profile(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE)
	image = models.ImageField(default='batman.png')

	def __str__(self):
		return f'Perfil de {self.user.username}'

	def following(self):
		user_ids = Relationship.objects.filter(from_user=self.user)\
								.values_list('to_user_id', flat=True)
		return User.objects.filter(id__in=user_ids)

	def followers(self):
		user_ids = Relationship.objects.filter(to_user=self.user)\
								.values_list('from_user_id', flat=True)
		return User.objects.filter(id__in=user_ids)


class Post(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')
	timestamp = models.DateTimeField(default=timezone.now)
	content = models.TextField()

	class Meta:
		ordering = ['-timestamp']

	def __str__(self):
		return f'{self.user.username}: {self.content}'


class Relationship(models.Model):
	from_user = models.ForeignKey(User, related_name='relationships', on_delete=models.CASCADE)
	to_user = models.ForeignKey(User, related_name='related_to', on_delete=models.CASCADE)

	def __str__(self): 
		return f'{self.from_user} to {self.to_user}'

	class Meta:
		indexes = [
		models.Index(fields=['from_user', 'to_user',]),
		]

class Producto(models.Model):
	nombre = models.CharField(max_length=100)
	descripcion = models.TextField()
	precio = models.DecimalField(max_digits=10, decimal_places=2)

	def __str__(self):
		return self.nombre


class CarritoItem(models.Model):
	usuario = models.ForeignKey(User, on_delete=models.CASCADE)
	producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
	cantidad = models.PositiveIntegerField(default=1)


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='profile_images/', blank=True, null=True) 

    def __str__(self):
        return self.user.username


