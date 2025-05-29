from django.db import models

class ExampleTableModel(models.Model):
    # Django automatically creates an 'id' primary key field
    name = models.CharField(max_length=100)
    value = models.IntegerField()
    # Add other fields corresponding to your table columns

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'example_table' # If your table already exists and has a specific name
        # managed = False # If Django should not manage this table's schema (e.g., for existing tables) - use with caution

class Event(models.Model):
    title = models.CharField(max_length=200)
    image = models.URLField(max_length=500)
    description = models.TextField()
    location = models.CharField(max_length=255)
    host = models.CharField(max_length=100)
    signups = models.PositiveIntegerField(default=0)
    distance = models.FloatField(help_text="Distance in miles or kilometers")
    date = models.DateField()
    time = models.TimeField()
    accepted = models.BooleanField(default=False)

    def __str__(self):
        return self.title