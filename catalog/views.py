from django.shortcuts import render,get_object_or_404,redirect
from django.views import generic
from .models import Book, Author, Genre, BookInstance
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from .forms import RenewBookForm
from django.contrib.auth.decorators import permission_required
from django.http import HttpResponseRedirect
from django.urls import reverse,reverse_lazy
from django.views.generic.edit import CreateView, UpdateView,DeleteView
import datetime

def index(req):
    num_books = Book.objects.all().count()
    num_instances = BookInstance.objects.all().count()
    num_authors = Author.objects.all().count()
    num_instances_available = BookInstance.objects.filter(status='a').count()
    word_b = 'Гарри'
    word_g = 'По'

    num_books_word = Book.objects.filter(title__icontains=word_b).count()
    num_genres_word = Genre.objects.filter(name__icontains=word_g).count()
    num_visits = req.session.get('num_visits', 0)
    req.session['num_visits'] = num_visits + 1


    return render(req, 'index/index.html', locals())

class BookListView(generic.ListView):
    model = Book
    template_name = 'catalog/book_list.html'
    paginate_by = 5

class BookDetailView(generic.DetailView):
    model = Book
    template_name = 'catalog/book_detail.html'
class AuthorListView(generic.ListView):
    model = Author
    template_name = 'catalog/author_list.html'
    paginate_by = 5

class AuthorDetailView(generic.DetailView):
    model = Author
    template_name = 'catalog/author_detail.html'

class LoanedBooksByUserListView(LoginRequiredMixin,generic.ListView):
    """
    Generic class-based view listing books on loan to current user.
    """
    model = BookInstance
    template_name ='catalog/bookinstance_list_borrowed_user.html'
    paginate_by = 3
    def get_queryset(self):

        return BookInstance.objects.filter(borrower=self.request.user).filter(status__exact='o').order_by('due_back')
# Create your views here.
class BorrowedListView(UserPassesTestMixin,generic.ListView):
    model = BookInstance
    template_name = 'catalog/all_borrowed_books.html'
    paginate_by = 5
    permission_required = 'catalog.can_mark_returned'

    def get_queryset(self):
        return BookInstance.objects.filter(status__exact='o').order_by('due_back')
    def test_func(self):
        return self.request.user.is_staff



@permission_required('catalog.can_mark_returned')
def renew_book_librarian(request,pk):
    bookinst = get_object_or_404(BookInstance, pk=pk)

    # Если данный запрос типа POST, тогда
    if request.method == 'POST':
        # Создаем экземпляр формы и заполняем данными из запроса(связывание, binding):
        form = RenewBookForm(request.POST)
        # Проверка валидности данных формы:
        if form.is_valid():
            # Обработка данных из form.cleaned_data
            # (здесь мы просто присваиваем их полю due_back)
            bookinst.due_back = form.cleaned_data['renewal_date']
            bookinst.save()
            # Переход по адресу 'all-borrowed':
            return HttpResponseRedirect(reverse('all-borrowed'))
    # Если это GET (или какой-либо еще), создать форму по умолчанию.
    else:
        proposed_renewal_date = datetime.date.today() + datetime.timedelta(weeks=3)
        form = RenewBookForm(initial={'renewal_date':
                                      proposed_renewal_date, })
    return render(request, 'catalog/book_renew_librarian.html', locals())

class AuthorCreate(LoginRequiredMixin,UserPassesTestMixin,CreateView):
    model = Author
    fields = '__all__'
    success_url = reverse_lazy('authors')
    initial={'date_of_death':'12/10/2016',}
    def test_func(self):
        return self.request.user.is_staff
    def handle_no_permission(self):
        return HttpResponseRedirect(reverse('login')+'?next=/catalog/authors/create/')

class AuthorUpdate(UpdateView):
    model = Author
    fields = ['first_name','last_name','date_of_birth','date_of_death']
class AuthorDelete(DeleteView):
    model = Author
    success_url = reverse_lazy('authors')
class BookCreate(CreateView):
    model = Book
    fields = '__all__'

class BookUpdate(UpdateView):
    model = Book
    fields = '__all__'
class BookDelete(DeleteView):
    model = Book
    success_url = reverse_lazy('books')