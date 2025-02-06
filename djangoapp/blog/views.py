from django.shortcuts import render

# Create your views here.


def index(request):
    return render(
        request=request,
        template_name="blog/pages/index.html"
    )


def post(request):
    return render(
        request=request,
        template_name="blog/pages/post.html"
    )


def page(request):
    return render(
        request=request,
        template_name="blog/pages/page.html"
    )
