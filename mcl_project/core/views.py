from django.shortcuts import render, redirect
from core.models import TeamDetails, BidTransactions, PlayerDetails, ManagerDetails
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required, user_passes_test
from django.db import models
from django.db.models import OuterRef, Exists
from django.contrib.auth import authenticate, login, logout
import random

# Create your views here.
def index(request):
    return render(request,'biddingWindow.html')

@login_required
@user_passes_test(lambda u: u.is_staff)
def admin_site(request):
    transactionsData = BidTransactions.objects.all()
    teamData = TeamDetails.objects.all()
    context = {
        'teams' : teamData,
        'transactions' : transactionsData,
        }
    return render(request,'admin.html', context)

def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            if user.is_staff:
                return redirect('admin-site')  # Redirect to admin site for superusers
            else:
                return redirect('teamlist')  # Redirect to a page after successful login
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

@login_required
def teamList(request):
    Team = TeamDetails.objects.filter(TeamName = request.user.username).first()
    Players = BidTransactions.objects.filter(Team=Team).exclude(T_status=0)
    Managers = ManagerDetails.objects.filter(team=Team)
    spent_price = BidTransactions.objects.filter(Team=Team, T_status=2).aggregate(total=models.Sum('price'))['total'] or 0
    context = {'team' : Team,
            'players' : Players,
            'managers' : Managers,
            'price_re' : 3000 - spent_price
           }
    return render(request,'teamlist.html',context)

def all_bids(request):
    all_sold_bids = BidTransactions.objects.filter(T_status=2).order_by('-T_ID')
    all_unsold_bids = BidTransactions.objects.filter(T_status=1).order_by('-T_ID')
    context = {
        'soldbids' : all_sold_bids,
        'unsoldbids' : all_unsold_bids 
    }
    return render(request,'allBids.html',context)


#################### API VIEWS ####################
from django.http import JsonResponse
from .models import TeamDetails, BidTransactions, ManagerDetails

def getTeamData(request, id):
    try:
        team = TeamDetails.objects.get(id=id)
    except TeamDetails.DoesNotExist:
        return JsonResponse({"error": "Team not found"}, status=404)

    # Calculate remaining price
    spent_price = BidTransactions.objects.filter(Team=team, T_status=2).aggregate(total=models.Sum('price'))['total'] or 0
    remaining_price = 3000 - spent_price

    # Serialize players
    players_qs = BidTransactions.objects.filter(Team=team).exclude(T_status=0)
    players = list(players_qs.values('playername__P_ID', 'playername__Name', 'playername__PlayerRole', 'price'))  # adjust fields as needed
    # Serialize managers
    managers_qs = ManagerDetails.objects.filter(team=team)
    managers = list(managers_qs.values('Name','Dept','Batch'))  # adjust fields as needed

    data = {
        "team_name": team.TeamName,
        "team_logo_url": team.TeamLogo.url if team.TeamLogo else None,
        "players": players,
        "manager": managers,
        "price_re": remaining_price,
    }

    return JsonResponse(data)


def get_random_player(request):

    used_players = BidTransactions.objects.filter(
        playername=OuterRef('pk')
    )

    player_qs = PlayerDetails.objects.annotate(
        already_used=Exists(used_players)
    ).filter(already_used=False)

    count = player_qs.count()

    if count == 0:
        return JsonResponse({"error": "No available players"}, status=404)

    random_index = random.randint(0, count - 1)
    player = player_qs[random_index]

    return JsonResponse({
        "player_id": player.P_ID,
        "name": player.Name,
    })

def get_pending_player(request):
    player_tran = BidTransactions.objects.filter(T_status=0).first()
    if player_tran:
        player = player_tran.playername
        data = {
            "player_id": player.P_ID,
            "name": player.Name,
            "current_bid" : player_tran.price,
            "team_name" : player_tran.Team.TeamName,
        }
    else:
        data = {
            "player_id": None,
            "name": None,
        }
    return JsonResponse(data)

def get_last_transaction_player(request):
    player_tran = BidTransactions.objects.order_by('-T_ID').first()
    if player_tran:
        player = player_tran.playername
        try:
            teamName = player_tran.Team.TeamName
        except:
            teamName = "NIL"
        data = {
            "player_id": player.P_ID,
            "name": player.Name,
            "bid_price" : player_tran.price,
            "team_name" : teamName,
            "photo_url": player.PlayerPhoto.url,
            "wicket_keeping" : "Yes" if player.WicketKeeping else "No",
            "role": player.PlayerRole,
            "dept": player.Dept,
            "batch": player.Batch,
            "bidState" : player_tran.T_status
        }
    else:
        data = {
            "player_id": None,
        }
    return JsonResponse(data)

def useful_counter(request):
    data = {
        "totalPlayer": PlayerDetails.objects.count(),
        "totalTeams": TeamDetails.objects.count(),
        "totalBids": BidTransactions.objects.count(),
        "totalPendingBids": BidTransactions.objects.filter(T_status=0).count(),
    }
    return JsonResponse(data)
