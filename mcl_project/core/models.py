from django.db import models
from django.contrib.auth.models import User
from cloudinary.models import CloudinaryField

# ---------------------------------------------------
# PLAYER DETAILS MODEL
# ---------------------------------------------------
class PlayerDetails(models.Model):
    Name  = models.CharField(max_length=25)
    Dept  = models.CharField(max_length=25)
    Batch = models.CharField(max_length=25)

    PlayerPhoto = CloudinaryField('player_photo', blank=True, null=True)
    PlayerRole  = models.CharField(max_length=25)
    WicketKeeping = models.BooleanField(choices=[(True, 'Yes'), (False, 'No')])

    P_ID = models.CharField(max_length=10, primary_key=True, unique=True, editable=False)

    def save(self, *args, **kwargs):
        if not self.P_ID:
            last_player = PlayerDetails.objects.order_by('-P_ID').first()
            if last_player:
                last_id = int(last_player.P_ID[1:])
                new_id = f'P{last_id + 1:03d}'
            else:
                new_id = 'P001'
            self.P_ID = new_id

        super().save(*args, **kwargs)

    def __str__(self):
        return self.P_ID

# ---------------------------------------------------
# TEAM DETAILS MODEL
# ---------------------------------------------------
class TeamDetails(models.Model):
    TeamName = models.CharField(max_length=25)
    HM_USER = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)    

    TeamHeadManager = models.CharField(max_length=25)
    TeamPlayingManager = models.CharField(max_length=25, default='none')
    TeamMarquee = models.CharField(max_length=25, default='none')
    TeamRetainedPlayer = models.CharField(max_length=25, default='none')
    
    TeamLogo = models.ImageField(upload_to='teamLogo/')

    def __str__(self):
        return self.TeamName

# ---------------------------------------------------
# MANAGER DETAILS MODEL (FIXED)
# ---------------------------------------------------
class ManagerDetails(models.Model):     # ❌ previously used models.Manager (wrong)
    Name  = models.CharField(max_length=25)
    Dept  = models.CharField(max_length=25)
    Batch = models.CharField(max_length=25)

    # Manager belongs to a team ✔
    team = models.ForeignKey(TeamDetails, on_delete=models.CASCADE)

    def __str__(self):
        return self.Name  

# ---------------------------------------------------
# BID TRANSACTIONS MODEL
# ---------------------------------------------------
class BidTransactions(models.Model):
    playername = models.OneToOneField(PlayerDetails, on_delete=models.CASCADE)
    price = models.IntegerField()  # ❌ IntegerField does NOT support max_length
    Team = models.ForeignKey(TeamDetails, on_delete=models.CASCADE, null=True,)

    T_ID = models.CharField(max_length=10, unique=True, primary_key=True, editable=False)
    T_status = models.IntegerField(default=0, choices=[(0, "Pending"), (1, "UnSold"), (2, "Sold")])
    def save(self, *args, **kwargs):
        if not self.T_ID:
            last_tran = BidTransactions.objects.order_by('-T_ID').first()
            if last_tran:
                last_id = int(last_tran.T_ID[1:])
                new_id = f'T{last_id + 1:03d}'
            else:
                new_id = 'T001'
            self.T_ID = new_id

        super().save(*args, **kwargs)

    def __str__(self):
        return self.T_ID
