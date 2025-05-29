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

class EventSignUpModel(models.Model):
    eventId = models.IntegerField()
    signUps = models.IntegerField()
    signedUp = models.BooleanField()

    def __str__(self):
        return f"Event ID: {self.eventId} - SignUps: {self.signUps} - signedUp: {self.signedUp}"
    
    class Meta:
        db_table = 'EventSignUp'
