Creating a Django-based job board involves designing job listings, adding filters, implementing search functionality, allowing users to submit and edit job postings, and creating a user profile section. Here’s a detailed plan for each task:

### 1. Design and Implement a Job Listing Page

**Steps:**
- Create a model for job postings.
- Implement views to display job listings.
- Design a template to render job listings.

**Example:**
```python
# models.py
from django.db import models

class Job(models.Model):
    title = models.CharField(max_length=100)
    company = models.CharField(max_length=100)
    location = models.CharField(max_length=100)
    category = models.CharField(max_length=50)
    description = models.TextField()
    posted_on = models.DateTimeField(auto_now_add=True)

# views.py
from django.shortcuts import render
from .models import Job

def job_list(request):
    jobs = Job.objects.all().order_by('-posted_on')
    return render(request, 'job_list.html', {'jobs': jobs})

# urls.py
from django.urls import path
from .views import job_list

urlpatterns = [
    path('', job_list, name='job_list'),
]
```

**Template:**
```html
<!-- templates/job_list.html -->
<!DOCTYPE html>
<html>
<head>
    <title>Job Board</title>
    <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.3.1/css/bootstrap.min.css">
</head>
<body>
    <div class="container">
        <h1>Job Listings</h1>
        <div class="row">
            {% for job in jobs %}
            <div class="col-md-4">
                <div class="card mb-4">
                    <div class="card-body">
                        <h5 class="card-title">{{ job.title }}</h5>
                        <p class="card-text">{{ job.company }} - {{ job.location }}</p>
                        <p class="card-text">{{ job.category }}</p>
                        <p class="card-text">{{ job.description|truncatewords:20 }}</p>
                        <a href="#" class="btn btn-primary">View Details</a>
                    </div>
                </div>
            </div>
            {% endfor %}
        </div>
    </div>
</body>
</html>
```

### 2. Add Filters for Job Categories and Locations

**Steps:**
- Update the view to handle filtering.
- Add filter forms to the template.

**Example:**
```python
# views.py
def job_list(request):
    category = request.GET.get('category')
    location = request.GET.get('location')
    jobs = Job.objects.all()

    if category:
        jobs = jobs.filter(category=category)
    if location:
        jobs = jobs.filter(location=location)

    return render(request, 'job_list.html', {'jobs': jobs})

# Add categories and locations to the template for filtering
categories = Job.objects.values_list('category', flat=True).distinct()
locations = Job.objects.values_list('location', flat=True).distinct()
```

**Template:**
```html
<!-- Add filter forms to job_list.html -->
<form method="GET" action="{% url 'job_list' %}">
    <select name="category">
        <option value="">All Categories</option>
        {% for category in categories %}
        <option value="{{ category }}">{{ category }}</option>
        {% endfor %}
    </select>
    <select name="location">
        <option value="">All Locations</option>
        {% for location in locations %}
        <option value="{{ location }}">{{ location }}</option>
        {% endfor %}
    </select>
    <button type="submit" class="btn btn-primary">Filter</button>
</form>
```

### 3. Implement a Search Functionality for Job Titles

**Steps:**
- Update the view to handle search queries.
- Add a search form to the template.

**Example:**
```python
# views.py
def job_list(request):
    category = request.GET.get('category')
    location = request.GET.get('location')
    search_query = request.GET.get('search')
    jobs = Job.objects.all()

    if category:
        jobs = jobs.filter(category=category)
    if location:
        jobs = jobs.filter(location=location)
    if search_query:
        jobs = jobs.filter(title__icontains=search_query)

    return render(request, 'job_list.html', {'jobs': jobs})
```

**Template:**
```html
<!-- Add search form to job_list.html -->
<form method="GET" action="{% url 'job_list' %}">
    <input type="text" name="search" placeholder="Search job titles">
    <button type="submit" class="btn btn-primary">Search</button>
</form>
```

### 4. Allow Users to Submit and Edit Job Postings

**Backend:**
- Create forms for job submissions.
- Implement views to handle job submissions and edits.

**Example:**
```python
# forms.py
from django import forms
from .models import Job

class JobForm(forms.ModelForm):
    class Meta:
        model = Job
        fields = ['title', 'company', 'location', 'category', 'description']

# views.py
from django.shortcuts import render, redirect
from .forms import JobForm

def submit_job(request):
    if request.method == 'POST':
        form = JobForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('job_list')
    else:
        form = JobForm()
    return render(request, 'submit_job.html', {'form': form})

def edit_job(request, job_id):
    job = Job.objects.get(id=job_id)
    if request.method == 'POST':
        form = JobForm(request.POST, instance=job)
        if form.is_valid():
            form.save()
            return redirect('job_list')
    else:
        form = JobForm(instance=job)
    return render(request, 'edit_job.html', {'form': form})
```

**Template:**
```html
<!-- templates/submit_job.html -->
<!DOCTYPE html>
<html>
<head>
    <title>Submit Job</title>
    <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.3.1/css/bootstrap.min.css">
</head>
<body>
    <div class="container">
        <h1>Submit Job</h1>
        <form method="POST">
            {% csrf_token %}
            {{ form.as_p }}
            <button type="submit" class="btn btn-primary">Submit</button>
        </form>
    </div>
</body>
</html>

<!-- templates/edit_job.html -->
<!DOCTYPE html>
<html>
<head>
    <title>Edit Job</title>
    <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.3.1/css/bootstrap.min.css">
</head>
<body>
    <div class="container">
        <h1>Edit Job</h1>
        <form method="POST">
            {% csrf_token %}
            {{ form.as_p }}
            <button type="submit" class="btn btn-primary">Save</button>
        </form>
    </div>
</body>
</html>
```

### 5. Create a Responsive and Visually Appealing User Profile Section

**Backend:**
- Create a model for user profiles.
- Implement views to display and edit profiles.

**Example:**
```python
# models.py
from django.contrib.auth.models import User

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField()
    profile_image = models.ImageField(upload_to='profile_images/', null=True, blank=True)

# forms.py
class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['bio', 'profile_image']

# views.py
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Profile
from .forms import ProfileForm

@login_required
def profile_view(request):
    profile, created = Profile.objects.get_or_create(user=request.user)
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('profile_view')
    else:
        form = ProfileForm(instance=profile)
    return render(request, 'profile.html', {'form': form, 'profile': profile})

# urls.py
from django.urls import path
from .views import profile_view

urlpatterns = [
    path('profile/', profile_view, name='profile_view'),
]
```

**Template:**
```html
<!-- templates/profile.html -->
<!DOCTYPE html>
<html>
<head>
    <title>User Profile</title>
    <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.3.1/css/bootstrap.min.css">
</head>
<body>
    <div class="container">
        <h1>User Profile</h1>
        <div class="row">
            <div class="col-md-4">
                <img src="{{ profile.profile_image.url }}" alt="Profile Image" class="img-fluid">
            </div>
            <div class="col-md-8">
                <form method="POST" enctype="multipart/form-data">
                    {% csrf_token %}
                    {{ form.as_p }}
                    <button type="submit" class="btn btn-primary">Save</button>
                </form>
            </div>
        </div>
    </div>
</body>
</html>
```

This setup provides a comprehensive solution for a Django-based job board, including job listings, filters, search functionality, job submissions, and a user profile section. Adjustments might be necessary based on specific requirements and preferences.