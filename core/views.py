from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout
from .models import Materia, Tarea, SesionPomodoro
from django.utils import timezone
from datetime import timedelta

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('dashboard')
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})

def register_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('dashboard')
    else:
        form = UserCreationForm()
    return render(request, 'register.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('login')

def dashboard(request):
    if not request.user.is_authenticated:
        return redirect('login')

    if request.method == 'POST':
        
        if 'nueva_materia' in request.POST:
            Materia.objects.create(nombre=request.POST['nombre_materia'], usuario=request.user)
        
        elif 'nueva_tarea' in request.POST:
            Tarea.objects.create(
                titulo=request.POST['titulo_tarea'], 
                materia_id=request.POST.get['materia_id'], 
                usuario=request.user
            )

        elif 'guardar_pomodoro' in request.POST:
            SesionPomodoro.objects.create(usuario=request.user, duracion_minutos=25)
        return redirect('dashboard')

    if 'completar_id' in request.GET:
        tarea = Tarea.objects.get(id=request.GET['completar_id'], usuario=request.user)
        tarea.completada = True
        tarea.fecha_completado = timezone.now()
        tarea.save()
        return redirect('dashboard')

    materias = Materia.objects.filter(usuario=request.user)
    tareas = Tarea.objects.filter(usuario=request.user).order_by('-id')

    hoy = timezone.now().date()
    tareas_hoy = Tarea.objects.filter(usuario=request.user, completada=True, fecha_completado__date=hoy).count()
    pomodoros_hoy = SesionPomodoro.objects.filter(usuario=request.user, fecha__date=hoy).count()

    labels = []
    data_tareas = []
    for i in range(6, -1, -1):
        dia = hoy - timedelta(days=i)
        labels.append(dia.strftime('%a'))
        data_tareas.append(Tarea.objects.filter(usuario=request.user, completada=True, fecha_completado__date=dia).count())

    racha = 0
    dia_check = hoy
    while True:
        hubo_actividad = Tarea.objects.filter(usuario=request.user, completada=True, fecha_completado__date=dia_check).exists() or \
                         SesionPomodoro.objects.filter(usuario=request.user, fecha__date=dia_check).exists()
        if hubo_actividad:
            racha += 1
            dia_check -= timedelta(days=1)
        else:
            break

    contexto = {
        'materias': materias, 'tareas': tareas,
        'tareas_hoy': tareas_hoy, 'pomodoros_hoy': pomodoros_hoy,
        'labels': labels, 'data_tareas': data_tareas, 'racha': racha
    }
    return render(request, 'dashboard.html', contexto)
