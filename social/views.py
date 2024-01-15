from django.shortcuts import render, redirect, get_object_or_404
from .models import *
from .forms import UserRegisterForm, PostForm, ProfilePhotoForm
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from .models import Producto, CarritoItem
from django.conf import settings
from paypalrestsdk import Payment
from django.http import JsonResponse


def feed(request):
	posts = Post.objects.all()

	context = { 'posts': posts}
	return render(request, 'social/feed.html', context) 

def register(request):
	if request.method == 'POST':
		form = UserRegisterForm(request.POST)
		if form.is_valid():
			form.save()
			username = form.cleaned_data['username']
			messages.success(request, f'Usuario {username} creado')
			return redirect('feed')
	else:
		form = UserRegisterForm()

	context = { 'form' : form }
	return render(request, 'social/register.html', context)


@login_required
def post(request):
	current_user = get_object_or_404(User, pk=request.user.pk)
	if request.method == 'POST':
		form = PostForm(request.POST)
		if form.is_valid():
			post = form.save(commit=False)
			post.user = current_user
			post.save()
			messages.success(request, 'Post enviado')
			return redirect('feed')
	else:
		form = PostForm()
	return render(request, 'social/post.html', {'form' : form })



def profile(request, username=None):
	current_user = request.user
	if username and username != current_user.username:
		user = User.objects.get(username=username)
		posts = user.posts.all()
	else:
		posts = current_user.posts.all()
		user = current_user
	return render(request, 'social/profile.html', {'user':user, 'posts':posts})



def edit_profile_photo(request):
    if request.method == 'POST':
        form = ProfilePhotoForm(request.POST, request.FILES, instance=request.user.profile)
        if form.is_valid():
            form.save()
            return redirect('profile')  # Reemplaza 'profile' con el nombre de la vista de perfil
    else:
        form = ProfilePhotoForm(instance=request.user.profile)

    return render(request, 'profile.html', {'form': form})


def follow(request, username):
	current_user = request.user
	to_user = User.objects.get(username=username)
	to_user_id = to_user
	rel = Relationship(from_user=current_user, to_user=to_user_id)
	rel.save()
	messages.success(request, f'sigues a {username}')
	return redirect('feed')

def unfollow(request, username):
	current_user = request.user
	to_user = User.objects.get(username=username)
	to_user_id = to_user.id
	rel = Relationship.objects.filter(from_user=current_user.id, to_user=to_user_id).get()
	rel.delete()
	messages.success(request, f'Ya no sigues a: {username}')
	return redirect('feed')


def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data['username']

            # Enviar correo de bienvenida
            subject = 'Bienvenido a la red social'
            message = f'Hola {username}, ¡Gracias por registrarte en nuestra red social!'
            from_email = 'uriel.bt.le@gmail.com'  
            to_email = [user.email]  

            send_mail(subject, message, from_email, to_email, fail_silently=True)

            messages.success(request, f'Usuario {username} creado')
            return redirect('feed')
    else:
        form = UserRegisterForm()

    context = {'form': form}
    return render(request, 'social/register.html', context)

def lista_productos(request):
	productos = Producto.objects.all()
	return render (request, 'social/lista_productos.html', {'productos': productos})

def detalle_producto(request, producto_id):
	producto = Producto.objects.get(pk=producto_id)
	return render(request, 'social/detalle_producto.html', {'producto': producto})

def add_to_cart(request, producto_id):
	producto = get_object_or_404(Producto, pk=producto_id)

	#verificar si el producto ya esra en el carrito
	carrito_item, created = CarritoItem.objects.get_or_create(
		usuario=request.user,
		producto=producto
	)
	#si ya eciste incrementa la cantidad de lo contrario crea uno nuevo
	if not created:
		carrito_item.cantidad +=1
		carrito_item.save()

	return redirect('view_cart')

def view_cart(request):
	carrito_items = CarritoItem.objects.filter(usuario=request.user)
	total = sum(item.producto.precio * item.cantidad for item in carrito_items)

	return render(request, 'social/view_cart.html', {'carrito_items': carrito_items, 'total':total})



def checkout(request):
    carrito_items = CarritoItem.objects.filter(usuario=request.user)
    total = sum(item.producto.precio * item.cantidad for item in carrito_items)

    # Lógica para crear un pago con PayPal
    payment = Payment({
        "intent": "sale",
        "payer": {
            "payment_method": "paypal",
        },
        "transactions": [
            {
                "amount": {
                    "total": f"{total:.2f}",
                    "currency": "USD",
                },
                "description": "Compra en tu tienda",
                "item_list": {
                    "items": [
                        {
                            "name": item.producto.nombre,
                            "price": str(item.producto.precio),
                            "currency": "USD",
                            "quantity": str(item.cantidad),
                        } for item in carrito_items
                    ],
                },
            },
        ],
        "redirect_urls": {
            "return_url": f"{settings.SITE_URL}/execute_payment/",
            "cancel_url": f"{settings.SITE_URL}/cancel_payment/",
        },
    })

    if payment.create():
        return redirect(payment.links[1].href)
    else:
        return render(request, 'social/error.html', {'error': payment.error})




def agregar_carrito(request, producto_id):
    producto = get_object_or_404(Producto, pk=producto_id)

    response_data = {'message': 'Producto añadido al carrito', 'producto_nombre': 'Nombre del Producto'}
    return JsonResponse(response_data)
