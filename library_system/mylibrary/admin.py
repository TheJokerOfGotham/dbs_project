from django.contrib import admin

from mylibrary.models import Book, Librarian, Member, Manages, Transaction, Penalty, Report


# Register your models here.
admin.site.register(Book)

admin.site.register(Member)
admin.site.register(Manages)
admin.site.register(Transaction)
admin.site.register(Penalty)
admin.site.register(Report)
class LibrarianAdmin(admin.ModelAdmin):
    list_display = ("user", "name", "email", "phone", "membership_date")
    search_fields = ("name", "email")

admin.site.register(Librarian, LibrarianAdmin)