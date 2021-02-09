# app/context_processors.py

def blogcategories(request):
    from olympicvaxinfo.models import Category
    return {'blogcategories': Category.objects.all().order_by('-name')}