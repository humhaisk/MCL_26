from django.shortcuts import render, redirect
from core.models import TeamDetails
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required

from django.contrib.auth import authenticate, login, logout

# Create your views here.
def index(request):
    return render(request,'biddingWindow.html')

@login_required
def admin_site(request):
    return render(request,'admin.html')

def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('admin-site')  # Redirect to a page after successful login
        else:
            print("LOST")
            return render(request, 'login.html', {'error_message': 'Invalid credentials'})
    else:
        return render(request, 'login.html')
    # return render(request,'login.html')

def user_logout(request):
    """Logs the user out and redirects to the login page."""
    # Use the imported and renamed function: auth_logout
    logout(request) 
    # Redirect to the login page after logging out
    return redirect('login')

def teamList(request):
    all_team = TeamDetails.objects.all()
    context = {'teams' : all_team}
    return render(request,'teamlist.html',context)

def getTeamData(request, id):
    team = TeamDetails.objects.get(id=id)
    data = {
        "team_name": team.TeamName,
        "team_logo_url": team.TeamLogo.url,
    }
    return JsonResponse(data)