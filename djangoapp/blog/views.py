from typing import Any

from django.shortcuts import redirect
from blog.models import Post, Page
from django.db.models import Q, QuerySet
from django.contrib.auth.models import User
from django.http import Http404, HttpRequest
from django.views.generic import ListView, DetailView

# Create your views here.

PER_PAGE = 9


class PostListView(ListView):  # Index Class Based View
    # model = Post
    template_name = 'blog/pages/index.html'
    context_object_name = "posts"
    # ordering = "-pk",
    paginate_by = PER_PAGE
    queryset = Post.objects.get_published()  # type: ignore

    # def get_queryset(self):
    #     queryset = super().get_queryset()
    #     queryset = queryset.filter(is_published=True)

    #     return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context.update({
            "page_title": "Home - ",
        })

        return context


# def index(request):
#     posts = Post.objects.get_published()  # type: ignore

#     paginator = Paginator(posts, PER_PAGE)
#     page_number = request.GET.get("page")
#     page_obj = paginator.get_page(page_number)

#     return render(
#         request,
#         'blog/pages/index.html',
#         {
#             'page_obj': page_obj,
#             "page_title": "Home - ",
#         }
#     )


class CreatedByListView(PostListView):
    def __init__(self, **kwargs: Any) -> None:
        super().__init__(**kwargs)

        self._temp_context: dict[str, Any] = {}

    def get_context_data(self, **kwargs) -> dict[str, Any]:
        ctx = super().get_context_data(**kwargs)

        user = self._temp_context["user"]

        user_full_name = user.username

        if user.first_name:
            user_full_name = f"{user.first_name} {user.last_name}"

        page_title = user_full_name + " - "

        ctx.update({
            "page_title": page_title,
        })

        return ctx

    def get_queryset(self) -> QuerySet:
        qs = super().get_queryset()
        qs = qs.filter(created_by__pk=self._temp_context["user"].pk)

        return qs

    def get(self, request: HttpRequest, *args, **kwargs):
        author_pk = self.kwargs.get("author_pk")
        user = User.objects.filter(pk=author_pk).first()

        if user is None:
            raise Http404()

        self._temp_context.update({
            "author_pk": author_pk,
            "user": user,
        })

        return super().get(request, *args, **kwargs)


# def created_by(request, author_pk):
#     user = User.objects.filter(pk=author_pk).first()

#     if user is None:
#         raise Http404()

#     posts = (
#         Post.objects.get_published()  # type: ignore
#         .filter(created_by__pk=author_pk)
#     )

#     user_full_name = user.username

#     if user.first_name:
#         user_full_name = f"{user.first_name} {user.last_name}"

#     page_title = user_full_name + " - "

#     paginator = Paginator(posts, PER_PAGE)
#     page_number = request.GET.get("page")
#     page_obj = paginator.get_page(page_number)

#     return render(
#         request,
#         'blog/pages/index.html',
#         {
#             'page_obj': page_obj,
#             "page_title": page_title,

#         }
#     )

class CategoryListView(PostListView):
    allow_empty = False

    def get_queryset(self):
        return super().get_queryset().filter(
            category__slug=self.kwargs.get("slug")
        )

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)

        page_title = f"{self.object_list[0].category.name} Category - "

        ctx.update({
            "page_title": page_title,
        })

        return ctx


# def category(request, slug):
#     posts = (
#         Post.objects.get_published()  # type: ignore
#         .filter(category__slug=slug)
#     )

#     paginator = Paginator(posts, PER_PAGE)
#     page_number = request.GET.get("page")
#     page_obj = paginator.get_page(page_number)

#     if len(page_obj) == 0:
#         raise Http404()

#     page_title = f"{page_obj[0].category.name} Category - "

#     return render(
#         request,
#         'blog/pages/index.html',
#         {
#             'page_obj': page_obj,
#             "page_title": page_title,
#         }
#     )

class TagListView(PostListView):
    allow_empty = False

    def get_queryset(self):
        return super().get_queryset().filter(
            tags__slug=self.kwargs.get("slug")
        )

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)

        tag_slug = self.kwargs.get("slug")
        tag_name = self.object_list[0].tags.filter(slug=tag_slug).first()
        page_title = f"{tag_name} Tag - "

        ctx.update({
            "page_title": page_title,
        })

        return ctx


# def tag(request, slug):
#     posts = (
#         Post.objects.get_published()  # type: ignore
#         .filter(tags__slug=slug)
#     )

#     paginator = Paginator(posts, PER_PAGE)
#     page_number = request.GET.get("page")
#     page_obj = paginator.get_page(page_number)

#     if len(page_obj) == 0:
#         raise Http404()

#     page_title = f"{page_obj[0].tags.filter(slug=slug).first().name} Tag - "

#     return render(
#         request,
#         'blog/pages/index.html',
#         {
#             'page_obj': page_obj,
#             "page_title": page_title,
#         }
#     )

class SearchListView(PostListView):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._search_value = ""

    def setup(self, request: HttpRequest, *args: Any, **kwargs: Any):
        self._search_value = request.GET.get("search", "").strip()
        return super().setup(request, *args, **kwargs)

    def get_queryset(self):
        search_value = self._search_value
        return super().get_queryset().filter(
            # Título contém search_value OU
            # Excerto contém search_value OU
            # Conteúdo contém search_value
            Q(title__icontains=search_value) |
            Q(excerpt__icontains=search_value) |
            Q(content__icontains=search_value)
        )[:PER_PAGE]

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)

        search_value = self._search_value

        ctx.update({
            "page_title": f"{search_value[:30]} Search - ",
            "search_value": search_value,
        })

        return ctx

    def get(self, request: HttpRequest, *args: Any, **kwargs: Any):
        if self._search_value == "":
            return redirect("blog:index")

        return super().get(request, *args, **kwargs)


# def search(request):
#     search_value = request.GET.get("search", "").strip()
#     posts = (
#         Post.objects.get_published()  # type: ignore
#         .filter(
#             # Título contém search_value OU
#             # Excerto contém search_value OU
#             # Conteúdo contém search_value
#             Q(title__icontains=search_value) |
#             Q(excerpt__icontains=search_value) |
#             Q(content__icontains=search_value)
#         )[:PER_PAGE]
#     )

#     # paginator = Paginator(posts, PER_PAGE)
#     # page_number = request.GET.get("page")
#     # page_obj = paginator.get_page(page_number)

#     page_title = f"{search_value[:30]} Search - "

#     return render(
#         request,
#         'blog/pages/index.html',
#         {
#             'page_obj': posts,
#             "page_title": page_title,
#             # 'page_obj': page_obj,
#             "search_value": search_value,
#         }
#     )


class PageDetailView(DetailView):
    model = Page
    template_name = "blog/pages/page.html"
    slug_field = "slug"
    context_object_name = "page"

    def get_context_data(self, **kwargs: Any):
        ctx = super().get_context_data(**kwargs)

        page = self.get_object()
        page_title = f"{page.title} - "

        ctx.update({
            "page_title": f"{page_title} - ",
        })

        return ctx

    def get_queryset(self):
        return super().get_queryset().filter(is_published=True)


# def page(request, slug):
#     page_obj = (
#         Page.objects
#         .filter(is_published=True)
#         .filter(slug=slug)
#         .first()
#     )

#     if page_obj is None:
#         raise Http404()

#     page_title = f"{page_obj.title} - "

#     return render(
#         request,
#         'blog/pages/page.html',
#         {
#             'page': page_obj,
#             "page_title": page_title,
#         }
#     )


class PostDetailView(DetailView):
    model = Post
    template_name = "blog/pages/post.html"
    slug_field = "slug"
    context_object_name = "post"

    def get_context_data(self, **kwargs: Any):
        ctx = super().get_context_data(**kwargs)

        post = self.get_object()
        page_title = f"{post.title} - "

        ctx.update({
            "page_title": f"{page_title} Post - ",
        })

        return ctx

    def get_queryset(self):
        return super().get_queryset().filter(is_published=True)


# def post(request, slug):
#     post_obj = (
#         Post.objects.get_published()  # type: ignore
#         .filter(slug=slug)
#         .first()
#     )

#     if post_obj is None:
#         raise Http404()

#     page_title = f"{post_obj.title} - "

#     return render(
#         request,
#         'blog/pages/post.html',
#         {
#             'post': post_obj,
#             "page_title": page_title,
#         }
#     )
