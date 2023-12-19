from django.db import models
from author.models import Author

class Book(models.Model):
    """
    This class represents a Book.
    Attributes:
    -----------
    param name: Describes name of the book
    type name: str max_length=128
    param description: Describes description of the book
    type description: str
    param count: Describes count of the book
    type count: int default=10
    param authors: list of Authors
    type authors: list->Author
    """

    name = models.CharField(max_length=128)
    description = models.TextField()
    count = models.IntegerField(default=10)
    authors = models.ManyToManyField(Author)

    def __str__(self):
        """
        Magic method is redefined to show all information about Book.
        :return: book id, book name, book description, book count, book authors
        """
        return f"'id': {self.id}, 'name': '{self.name}', 'description': '{self.description}', 'count': {self.count}, 'authors': {list(self.authors.values_list('id', flat=True))}"

    def __repr__(self):
        """
        This magic method is redefined to show class and id of Book object.
        :return: class, id
        """
        return f"Book(id={self.id})"

    @staticmethod
    def get_by_id(book_id):
        """
        :param book_id: SERIAL: the id of a Book to be found in the DB
        :return: book object or None if a book with such ID does not exist
        """
        try:
            return Book.objects.get(id=book_id)
        except Book.DoesNotExist:
            return None

    @staticmethod
    def delete_by_id(book_id):
        """
        :param book_id: an id of a book to be deleted
        :type book_id: int
        :return: True if object existed in the db and was removed or False if it didn't exist
        """
        try:
            book = Book.objects.get(id=book_id)
            book.delete()
            return True
        except Book.DoesNotExist:
            return False

    @staticmethod
    def create(name, description, count=10, authors=None):
        """
        :param name: Describes name of the book
        :type name: str max_length=128
        :param description: Describes description of the book
        :type description: str
        :param count: Describes count of the book
        :type count: int default=10
        :param authors: list of Authors
        :type authors: list->Author
        :return: a new book object which is also written into the DB
        """
        book = Book(name=name, description=description, count=count)
        book.save()
        if authors:
            book.authors.add(*authors)
        return book

    def to_dict(self):
        """
        :return: book id, book name, book description, book count, book authors
        :Example:
        | {
        |   'id': 8,
        |   'name': 'django book',
        |   'description': 'bla bla bla',
        |   'count': 10,
        |   'authors': [1, 2, 3]
        | }
        """
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'count': self.count,
            'authors': list(self.authors.values_list('id', flat=True)),
        }

    def update(self, name=None, description=None, count=None):
        """
        Updates book in the database with the specified parameters.\n
        :param name: Describes name of the book
        :type name: str max_length=128
        :param description: Describes description of the book
        :type description: str
        :param count: Describes count of the book
        :type count: int default=10
        :return: None
        """
        if name is not None:
            self.name = name
        if description is not None:
            self.description = description
        if count is not None:
            self.count = count
        self.save()

    def add_authors(self, authors):
        """
        Add authors to book in the database with the specified parameters.\n
        :param authors: list authors
        :type authors: list->Author
        :return: None
        """
        self.authors.add(*authors)

    def remove_authors(self, authors):
        """
        Remove authors from book in the database with the specified parameters.\n
        :param authors: list authors
        :type authors: list->Author
        :return: None
        """
        self.authors.remove(*authors)

    @staticmethod
    def get_all():
        """
        returns data for json request with QuerySet of all books
        """
        return Book.objects.all()
