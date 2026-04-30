from django.views.generic import ListView, DetailView
from django.db.models import Q
from .models import Audiobook, Genre

class BookListView(ListView):
    model = Audiobook
    template_name = 'catalog/book_list.html'
    context_object_name = 'books'
    paginate_by = 12

    def get_queryset(self):
        qs = Audiobook.objects.filter(is_published=True).order_by('-created_at')
        query = self.request.GET.get('q', '')
        if query:
            qs = qs.filter(Q(title__icontains=query) | Q(author__name__icontains=query))
        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['genres'] = Genre.objects.all()
        return context

class GenreListView(ListView):
    model = Audiobook
    template_name = 'catalog/book_list.html'
    context_object_name = 'books'
    paginate_by = 12

    def get_queryset(self):
        return Audiobook.objects.filter(
            is_published=True,
            genres__slug=self.kwargs['slug']
        ).order_by('-created_at')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['genres'] = Genre.objects.all()
        context['active_genre_slug'] = self.kwargs['slug']
        return context

class BookDetailView(DetailView):
    model = Audiobook
    template_name = 'catalog/book_detail.html'
    context_object_name = 'book'

    def get_queryset(self):
        return Audiobook.objects.filter(is_published=True)