from django.shortcuts import redirect, render

from apps.blog.models import BlogPost
from apps.users.models import User
from .forms import ContactForm


def index(request):
    all_posts = BlogPost.objects.live().filter(featured=False).order_by('-first_published_at')[:9]
    featured_posts = BlogPost.objects.live().order_by('-first_published_at').filter(featured=True)[:4]

    context = {
        'featured': featured_posts,
        'all_posts': all_posts,
        'owner': User.objects.first(),
        'title': 'Home'
    }

    return render(request, 'home/index.html', context)


def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            # send email
            # messages.success(request, "Thank you for your message! We'll get back to you ASAP.")
            return redirect('home:contact')
    else:
        form = ContactForm()

    context = {
        'form': form,
        'title': 'Contact'
    }

    return render(request, 'home/contact.html', context)
