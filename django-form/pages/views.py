from django.shortcuts import render, redirect
from .forms import StudentForm
from .models import Student


def add_student(request):
    if request.method == 'POST':
        form = StudentForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('student_list')
    else:
        form = StudentForm()
    return render(request, 'pages/form.html', {'form': form})


def student_list(request):
    students = Student.objects.all()
    return render(request, 'pages/table.html', {'students': students})
