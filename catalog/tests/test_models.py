from django.test import TestCase
from catalog.models import Author,Book, BookInstance
class AuthorModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):

        # Set up non-modified objects used by all test methods
        Author.objects.create(first_name='Big', last_name='Bob')

    def test_first_name_label(self):
        author = Author.objects.get(id=1)

        field_label = author._meta.get_field('first_name').verbose_name
        self.assertEquals(field_label, 'first name')

    def test_date_of_death_label(self):
        author = Author.objects.get(id=1)

        field_label = author._meta.get_field('date_of_death').verbose_name
        self.assertEquals(field_label, 'died')

    def test_first_name_max_length(self):
        author = Author.objects.get(id=1)

        max_length = author._meta.get_field('first_name').max_length
        self.assertEquals(max_length, 100)

    def test_object_name_is_last_name_comma_first_name(self):
        author = Author.objects.get(id=1)

        expected_object_name = '%s, %s' % (author.last_name,
                                           author.first_name)
        self.assertEquals(expected_object_name, str(author))

    def test_get_absolute_url(self):
        author = Author.objects.get(id=1)
        # This will also fail if the urlconf is not defined.
        self.assertEquals(author.get_absolute_url(), '/catalog/authors/1')

class BookModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):

        # Set up non-modified objects used by all test methods
        Book.objects.create(title = 'Анна каренина ', summary='У Анют постоянно какие то проблемы с рельсами ',
                            isbn= '1234567894562')
        Book.genre = "Роман"
        Book.save

    def test_title_label(self):
        book = Book.objects.get(id=1)

        field_label = book._meta.get_field('title').verbose_name
        self.assertEquals(field_label, 'title')

    def test_isbn_label(self):
        book = Book.objects.get(id=1)

        field_label = book._meta.get_field('isbn').verbose_name
        self.assertEquals(field_label, 'ISBN')

    def test_summary_max_length(self):
        book = Book.objects.get(id=1)

        max_length = book._meta.get_field('summary').max_length
        self.assertEquals(max_length, 1000)


    def test_get_absolute_url(self):
        book = Book.objects.get(id=1)
        # This will also fail if the urlconf is not defined.
        self.assertEquals(book.get_absolute_url(), '/catalog/books/1')

class BookInstanceModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):

        # Set up non-modified objects used by all test methods
        BookInstance.objects.create(imprint='AGV',due_back='2020-11-20')
    def test_imprint_label(self):
        book = BookInstance.objects.get(imprint='AGV')

        field_label = book._meta.get_field('imprint').verbose_name
        self.assertEquals(field_label, 'imprint')

    def test_book_label(self):
        book = BookInstance.objects.get(imprint='AGV')

        field_label = book._meta.get_field('book').verbose_name
        self.assertEquals(field_label, 'book')

    def test_is_overdue_url(self):
        book = BookInstance.objects.get(imprint='AGV')
        flag = book.is_overdue
        self.assertTrue(flag)

    def tets_presenting(self):
        book = BookInstance.objects.get(imprint='AGV')
        expect  = '{0} ({1})'.format(book.id, book.book.title)
        self.assertEquals(str(book),expect)
