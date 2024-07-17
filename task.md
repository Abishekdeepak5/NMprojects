Creating a Django-based task management app involves several steps to ensure a user-friendly and functional application. Here’s a high-level overview and some details for each task:

### 1. Design a User-Friendly Task List Interface

**Steps:**
- Use Django templates to create the HTML structure.
- Utilize CSS frameworks like Bootstrap for responsive and attractive design.
- Ensure the interface is clean, with clear buttons for adding, deleting, and marking tasks as completed.

**Example:**
```html
<!-- templates/task_list.html -->
<!DOCTYPE html>
<html>
<head>
    <title>Task Management</title>
    <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.3.1/css/bootstrap.min.css">
    <style>
        .completed { text-decoration: line-through; }
    </style>
</head>
<body>
    <div class="container">
        <h1>Task List</h1>
        <div id="task-list"></div>
        <form id="new-task-form">
            <input type="text" id="new-task" placeholder="Add a new task" required>
            <button type="submit" class="btn btn-primary">Add Task</button>
        </form>
    </div>
    <script src="https://code.jquery.com/jquery-3.3.1.slim.min.js"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/jqueryui/1.12.1/jquery-ui.min.js"></script>
    <script src="{% static 'js/tasks.js' %}"></script>
</body>
</html>
```

### 2. Implement Task Creation and Deletion Functionality

**Backend:**
- Create models for Task.
- Implement views to handle task creation and deletion.
- Use Django forms to handle input.

**Example:**
```python
# models.py
from django.db import models

class Task(models.Model):
    name = models.CharField(max_length=255)
    completed = models.BooleanField(default=False)

# views.py
from django.shortcuts import render, redirect
from .models import Task
from .forms import TaskForm

def task_list(request):
    tasks = Task.objects.all()
    return render(request, 'task_list.html', {'tasks': tasks})

def add_task(request):
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            form.save()
    return redirect('task_list')

def delete_task(request, task_id):
    task = Task.objects.get(id=task_id)
    task.delete()
    return redirect('task_list')

# forms.py
from django import forms
from .models import Task

class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['name']
```

### 3. Add Drag-and-Drop Functionality for Task Reordering

**Frontend:**
- Use jQuery UI for drag-and-drop functionality.
- Update the backend to handle the new order of tasks.

**Example:**
```javascript
// static/js/tasks.js
$(function() {
    $("#task-list").sortable({
        update: function(event, ui) {
            // Update the order in the backend
            var order = $(this).sortable('toArray');
            $.post('/update-task-order/', { order: order });
        }
    });
});
```

### 4. Provide the Ability to Mark Tasks as Completed

**Backend:**
- Add a view to toggle the completion status of a task.

**Example:**
```python
# views.py
def toggle_task_completion(request, task_id):
    task = Task.objects.get(id=task_id)
    task.completed = not task.completed
    task.save()
    return redirect('task_list')
```

**Frontend:**
- Add a checkbox or button to toggle task completion.
```html
<!-- task_list.html -->
{% for task in tasks %}
<div id="task-{{ task.id }}" class="task {% if task.completed %}completed{% endif %}">
    <input type="checkbox" onclick="toggleCompletion({{ task.id }})" {% if task.completed %}checked{% endif %}>
    {{ task.name }}
    <button onclick="deleteTask({{ task.id }})" class="btn btn-danger">Delete</button>
</div>
{% endfor %}
```

### 5. Implement Data Persistence Using Local Storage

If you want to keep it simple and use local storage instead of a database:

**Example:**
```javascript
// static/js/tasks.js
$(function() {
    loadTasks();

    $('#new-task-form').submit(function(event) {
        event.preventDefault();
        var taskName = $('#new-task').val();
        addTask(taskName);
        $('#new-task').val('');
    });
});

function loadTasks() {
    var tasks = JSON.parse(localStorage.getItem('tasks')) || [];
    tasks.forEach(function(task) {
        displayTask(task);
    });
}

function addTask(name) {
    var tasks = JSON.parse(localStorage.getItem('tasks')) || [];
    var task = { id: Date.now(), name: name, completed: false };
    tasks.push(task);
    localStorage.setItem('tasks', JSON.stringify(tasks));
    displayTask(task);
}

function displayTask(task) {
    var taskHtml = `<div id="task-${task.id}" class="task ${task.completed ? 'completed' : ''}">
        <input type="checkbox" onclick="toggleCompletion(${task.id})" ${task.completed ? 'checked' : ''}>
        ${task.name}
        <button onclick="deleteTask(${task.id})" class="btn btn-danger">Delete</button>
    </div>`;
    $('#task-list').append(taskHtml);
}

function toggleCompletion(id) {
    var tasks = JSON.parse(localStorage.getItem('tasks'));
    var task = tasks.find(t => t.id === id);
    task.completed = !task.completed;
    localStorage.setItem('tasks', JSON.stringify(tasks));
    $(`#task-${id}`).toggleClass('completed');
}

function deleteTask(id) {
    var tasks = JSON.parse(localStorage.getItem('tasks'));
    tasks = tasks.filter(t => t.id !== id);
    localStorage.setItem('tasks', JSON.stringify(tasks));
    $(`#task-${id}`).remove();
}
```

This setup combines Django for backend management and local storage for simple data persistence. For more advanced functionality or larger applications, consider using Django’s ORM and database capabilities for data persistence.