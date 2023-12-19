from django.db import models
from authentication.models import CustomUser
from book.models import Book
import datetime
import pytz

class Order(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    end_at = models.DateTimeField(null=True, blank=True)
    plated_end_at = models.DateTimeField()

    def __str__(self):
        return (
            f"'id': {self.id}, "
            f"'user': {repr(self.user)}, "
            f"'book': {repr(self.book)}, "
            f"'created_at': '{self.created_at}', "
            f"'end_at': {repr(self.end_at)}, "
            f"'plated_end_at': '{self.plated_end_at}'"
        )

    def __repr__(self):
        return f"{self.__class__.__name__}(id={self.id})"

    def to_dict(self):
        return {
            'id': self.id,
            'user': self.user.id,
            'book': self.book.id,
            'created_at': int(self.created_at.timestamp()),
            'end_at': int(self.end_at.timestamp()) if self.end_at else None,
            'plated_end_at': int(self.plated_end_at.timestamp())
        }

    @staticmethod
    def create(user, book, plated_end_at):
        if user.id is None or book.id is None:
            return None
        return Order.objects.create(user=user, book=book, plated_end_at=plated_end_at)

    @staticmethod
    def get_by_id(order_id):
        try:
            return Order.objects.get(id=order_id)
        except Order.DoesNotExist:
            return None

    def update(self, plated_end_at=None, end_at=None):
        if plated_end_at is not None:
            self.plated_end_at = plated_end_at
        if end_at is not None:
            self.end_at = end_at
        self.save()

    @staticmethod
    def get_all():
        return list(Order.objects.all())

    @staticmethod
    def get_not_returned_books():
        return list(Order.objects.filter(end_at__isnull=True))

    @staticmethod
    def delete_by_id(order_id):
        try:
            order = Order.objects.get(id=order_id)
            order.delete()
            return True
        except Order.DoesNotExist:
            return False
