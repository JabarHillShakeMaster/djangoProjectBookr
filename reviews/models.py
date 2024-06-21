from django.db import models
from django.contrib import auth
from django.http import HttpResponse
# Create your models here.

class Publisher(models.Model):
    """A Company that publishes  books."""
    name = models.CharField \
        (max_length=50, \
         help_text="The name of the Publisher.")
    website = models.URLField \
        (help_text="The Publisher's website.")
    email = models.EmailField \
        (help_text="The Publisher's email address.")

    def __str__(self):
        return self.name

class Book(models.Model):
    """A publisher book."""
    title = models.CharField \
        (max_length=70, \
         help_text="The title of the book.")
    edition = models.CharField \
        (max_length=10, \
         help_text="The edition of the book.")
    publication_date = models.DateField \
        (verbose_name=\
         "Date the book was published.")
    isbn = models.CharField \
        (max_length=20, \
         verbose_name="ISBN number of the book.")
    publisher = models.ForeignKey \
        (Publisher, on_delete=models.CASCADE)
    contributors = (models.ManyToManyField \
        ('Contributor', through="BookContributor"))

    def isbn13(selfself, obj):
        return "{}-{}-{}-{}-{}".format(obj.isbn[0:3], obj.isbn[3:4], obj.isbn[4:6], obj.isbn[6:12], obj.isbn[12:13])
    def __str__(self):
        return "{} ({})".format(self.title,self.isbn)

class Contributor(models.Model):
    """
    A Contributor to a Book, e.g auther, editor. \
    co-author.
    """
    first_name = models.CharField \
        (max_length=50, \
         help_text=\
         "The contributor's first name or names.")
    last_name = models.CharField \
        (max_length=50, \
         help_text=\
         "The contributor's last name or names.")
    email = models.EmailField \
        (help_text="The contact email for the contributor.")
    phoneNumber = models.CharField \
        (max_length=17, \
         help_text="The contact phone number for the contributor.")

    def initialled_name(obj):
        initials = ''.join([name[0] for name in obj.first_names.split(' ')])

        return "{}, {}".format(obj.last_names, initials)

    def __str__(self):
        return self.first_name

class BookContributor(models.Model):
    class ContributionRole(models.TextChoices):
        AUTHOR = "AUTHOR", "Author"
        CO_AUTHOR = "CO_AUTHOR", "Co-Author"
        EDITOR = "EDITOR", "Editor"

    book = models.ForeignKey \
        (Book, on_delete=models.CASCADE)
    contributor = models.ForeignKey \
        (Contributor, \
         on_delete=models.CASCADE)
    role = models.CharField \
        (verbose_name=\
         "The role this contributor had in the book.", \
         choices=ContributionRole.choices, max_length=20)

    def __str__(self):
        return "{} {} {}".format(self.contributor.initialled_name(), self.role, self.book.isbn)

class Review(models.Model):
    content = models.TextField(help_text="Review text")
    rating = models.IntegerField(help_text="Rating the reviewer has given")
    date_created = models.DateTimeField(auto_now_add=True,help_text= "Date and time the review was created")
    date_edited = models.DateTimeField(null=True, help_text='''Date and time the review was modified''')
    creator = models.ForeignKey(auth.get_user_model(), on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE, help_text="The Book this review is about")

    def __str__(self):
        return "{} - {}".format(self.creator.username, self.book.title)