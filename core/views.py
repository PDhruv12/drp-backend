from django.forms import model_to_dict
from django.http import JsonResponse

def my_api_endpoint(request):
  data = {'message': 'Hello from Django!'}
  return JsonResponse(data)

def alive(_):
  data = {'message': "yeah bro I'm still alive"}
  return JsonResponse(data)

# User sends post request with location
def get_data_from_db_orm(request):
  # This is a placeholder. You need to define YourTableModel in a models.py file.
  from models import YourTableModel # Import your model
  
  # Example: Fetch all records
  records = YourTableModel.objects.all()
  
  # Convert queryset to a list of dictionaries
  data = [model_to_dict(record) for record in records]
  
  # For now, returning a placeholder as YourTableModel is not fully set up in your current context
  data = [{'info': 'This endpoint would use Django ORM. Define YourTableModel first.'}]
  
  return JsonResponse(data, safe=False)

# You would then update your backend/urls.py to point to this new view