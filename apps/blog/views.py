from django.views.generic import ListView, DetailView
from django.views.generic.edit import FormMixin
from django.urls import reverse
from django.db.models import Q
from django.contrib import messages
from .models import BlogPost, Comment, Category, Tag
from .forms import CommentForm


class BlogListView(ListView):
    model = BlogPost
    template_name = "blog/blog_list.html"
    context_object_name = "posts"
    paginate_by = 9

    def get_queryset(self):
        queryset = BlogPost.objects.filter(is_published=True)
        query = self.request.GET.get("q")
        if query:
            queryset = queryset.filter(
                Q(title__icontains=query)
                | Q(excerpt__icontains=query)
                | Q(content__icontains=query)
            )
        category_slug = self.request.GET.get("category")
        if category_slug:
            queryset = queryset.filter(category__slug=category_slug)
        tag_slug = self.request.GET.get("tag")
        if tag_slug:
            queryset = queryset.filter(tags__slug=tag_slug)
        return queryset.order_by("-created_at")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["categories"] = Category.objects.all()
        context["tags"] = Tag.objects.filter(posts__is_published=True).distinct()
        context["list_meta_title"] = "Blog | Articles & Insights"
        context["list_meta_description"] = "Articles and insights on Python, RPA, backend development, and automation."
        context["list_meta_keywords"] = "blog, articles, python, rpa, backend, django, automation"
        return context


class BlogDetailView(FormMixin, DetailView):
    model = BlogPost
    template_name = "blog/blog_detail.html"
    context_object_name = "post"
    queryset = BlogPost.objects.filter(is_published=True)
    form_class = CommentForm

    def get_success_url(self):
        return reverse("blog_detail", kwargs={"slug": self.object.slug})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        post = self.object
        context["comments"] = post.comments.filter(is_active=True)
        context["form"] = self.get_form()
        context["canonical_url"] = self.request.build_absolute_uri(post.get_absolute_url())
        context["seo_title"] = post.meta_title or post.title
        context["seo_description"] = post.meta_description or post.excerpt
        _kw = post.meta_keywords
        if not _kw:
            _parts = []
            if post.category:
                _parts.append(post.category.name)
            _parts.extend([t.name for t in post.tags.all()])
            _kw = ", ".join(_parts)
        context["seo_keywords"] = _kw
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        return self.form_invalid(form)

    def form_valid(self, form):
        comment = form.save(commit=False)
        comment.post = self.object
        comment.save()
        messages.success(self.request, "Your comment has been submitted and is pending moderation.")
        return super().form_valid(form)
