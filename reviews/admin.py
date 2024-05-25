from django.contrib import admin
from django.contrib.admin import ModelAdmin
from reviews.models import Publisher, Contributor, Book, BookContributor, Review


class BookAdmin(admin.ModelAdmin):
    date_hierarchy = 'publication_date'
    list_display = ('title', 'isbn13')
    def isbn13(selfself, obj):
        return "{}-{}-{}-{}-{}".format(obj.isbn[0:3], obj.isbn[3:4], obj.isbn[4:6], obj.isbn[6:12], obj.isbn[12:13])
    list_filter = ('publisher', 'publication_date')
    search_fields = ('title', 'isbn', 'publisher_name_startwith')

def initialled_name(obj):
    initials = ''.join([name[0] for name in obj.first_name.split(' ')])

    return "{}, {}".format(obj.last_name, initials)

class ContributorAdmin(admin.ModelAdmin):
    list_display = ('last_name', 'first_name',)
    search_fields = ('last_name', 'first_name',)
    list_filter = ('last_name',)


class ReviewAdmin(admin.ModelAdmin):
    exclude = ('date_edited',)
    fields = ('content', 'rating', 'creator', 'book')
    #fieldsets = (('Review content', {'fields': ('creator', 'rating')}),)

# Register your models here.
admin.site.register(Publisher)
admin.site.register(Contributor, ContributorAdmin)
admin.site.register(Book, BookAdmin)
admin.site.register(BookContributor)
admin.site.register(Review, ReviewAdmin)
