from django.shortcuts import render, redirect
from .forms import UserForm,UserProfileInfoForm, LoginForm
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse
from django.urls import reverse
from django.contrib.auth.decorators import login_required#, permission_required
from .decorators.extensions import permission_required
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from django.http import FileResponse
import io
# Create your views here.

def index(request):
    context = {'download_pdf': request.user.has_perm("authenticate.download_pdf")}
    print(request.user.has_perm("authenticate.download_pdf"))
    return render(request,'index.html', context)

def register(request):
    registered = False
    if request.method == 'POST':
        user_form = UserForm(data=request.POST)
        profile_form = UserProfileInfoForm(data=request.POST)
        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()
            user.set_password(user.password)
            user.save()
            profile = profile_form.save(commit=False)
            profile.user = user
            if 'profile_image' in request.FILES:
                profile.profile_image = request.FILES['profile_image']
            profile.save()
            registered = True
        else:
            print(user_form.errors,profile_form.errors)
    else:
        user_form = UserForm()
        profile_form = UserProfileInfoForm()
    return render(request,'registration.html',
                          {'user_form':user_form,
                           'profile_form':profile_form,
                           'registered':registered})

def login_user(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        username = request.POST.get('username')
        password = request.POST.get('password')
        nextPage = request.POST.get('next')
        if form.is_valid():
            user = authenticate(username=username, password=password)
            if user is not None and user.is_active:
                login(request,user)
                request.session['myUserName'] = user.username
                request.session['myProfilePicture'] = user.userprofileinfo.showMyProfilePicture()
                if nextPage:
                    return redirect(nextPage)
                else:
                    return redirect("authenticate:index")
            else:
                return HttpResponse("Your account was inactive.")
    else:
        form = LoginForm
    return render(request, 'login.html', {'form':form})

@login_required
def validate_auth(request):
    return render(request, 'validate.html', {'message':"Solo los verdaderos profetas autenticados veran este mensaje !"})

@login_required
@permission_required(['authenticate.download_pdf'])
def export_pdf(request):
    c = canvas.Canvas("grilla-alumnos.pdf", pagesize=A4)
    w, h = A4
    max_rows_per_page = 45
    # Margin.
    x_offset = 50
    y_offset = 50
    # Space between rows.
    padding = 15
    
    xlist = [x + x_offset for x in [0, 200, 250, 300, 350, 400, 480]]
    ylist = [h - y_offset - i*padding for i in range(max_rows_per_page + 1)]
    
    for rows in range(1,100):
        rows = tuple(filter(bool, rows))
        c.grid(xlist, ylist[:len(rows) + 1])
        for y, row in zip(ylist[:-1], rows):
            for x, cell in zip(xlist, row):
                c.drawString(x + 2, y - padding + 3, str(cell))
        c.showPage()
    
    c.save()
    data = [("NOMBRE", "NOTA 1", "NOTA 2", "NOTA 3", "PROM.", "ESTADO")]
    for i in range(1, 101):
        exams = [randint(0, 10) for _ in range(3)]
        avg = round(mean(exams), 2)
        state = "Aprobado" if avg >= 4 else "Desaprobado"
        data.append((f"Alumno {i}", *exams, avg, state))
    export_to_pdf(data)

@login_required
def user_logout(request):
    logout(request)
    return redirect("authenticate:index")

    