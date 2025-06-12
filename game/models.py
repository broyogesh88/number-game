from django.db import models
from django.db.models import JSONField
import uuid

class Game(models.Model):
  game_code = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
  steps = models.IntegerField(default=10)
  parent_array = JSONField(default=list)
  current_turn = models.IntegerField(default=0)
  round = models.IntegerField(default=1)
  is_complete = models.BooleanField(default=False)
  winner = models.ForeignKey('Player', null=True, blank=True, on_delete=models.SET_NULL, related_name='won_games')

class Player(models.Model):
  game = models.ForeignKey(Game, related_name='players', on_delete=models.CASCADE)
  name = models.CharField(max_length=100)
  value = models.IntegerField(default=0)
  available_numbers = JSONField(default=list)
  operands = JSONField(default=dict)
  parent_used = models.IntegerField(default=0)
  player_index = models.IntegerField()  # 0 or 1
  has_moved = models.BooleanField(default=False)  