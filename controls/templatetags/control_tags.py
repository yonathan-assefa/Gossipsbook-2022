from django import template
from users.models import Interests
from gossips.models import GossipsModel
from cheaters.models import CheatersModel
from controls.helpers import get_trending
from questions.models import QuestionsModel



register = template.Library()

@register.simple_tag
def trending_gossips():
   return get_trending(GossipsModel)


@register.simple_tag
def trending_cheaters():
   return get_trending(CheatersModel)


@register.simple_tag
def trending_questions():
   return get_trending(section='question')


@register.simple_tag
def interests_all():
   interests = Interests.objects.all()
   return interests


