from django.shortcuts import render, get_object_or_404
from .models import Post
from django.core.paginator import Paginator, EmptyPage,\
    PageNotAnInteger
from django.views.generic import ListView
from .forms import EmailPostForm
from django.core.mail import send_mail


class PostListView(ListView):
    queryset = Post.published.all()
    context_object_name = 'posts'
    paginate_by = 3
    template_name = 'blog/post/list.html'

def post_share(request, post_id):
    #Retrieve post by Id
    sent = False
    post = get_object_or_404(Post, id=post_id, status='published')
    if request.method == 'POST':
        #Form was submitted
        form = EmailPostForm(request.POST)
        if form.is_valid():
            #Form fields Valid
            cleaned_data = form.cleaned_data
            #Send Email
            post_url  = request.build_absolute_uri(
                post.get_absolute_url())
            subject = f"{cleaned_data['name']} Recommends you read "\
                       f"{post.title}"
            message = f"Read {post.title} at {post_url}\n\n" \
                      f"{cleaned_data['name']} \'s comments: {cleaned_data['comments']}"
            
            send_mail(subject, message, 'yeku.wilfred@yahoo.com', [cleaned_data['to']])
            sent = True
    else:
        form = EmailPostForm()
    return render(request, 'blog/post/share.html', {'post': post,
                                                    'form': form,
                                                    'sent': sent})


def post_detail(request, year, month, day, post):
    post = get_object_or_404(Post, slug=post,
                             status='published',
                             publish__year=year,
                             publish__month=month,
                             publish__day=day)
    return render(request, 'blog/post/detail.html',
                  {'post': post}
                  )
