from django.db import models
from django.contrib.auth.models import User # really use django users?

VoteStates = {
	(1, u"Suggested"),
	(2, u"Voted"),
	(3, u"Frozen"),
	(4, u"FrozenSuggestion"),
	(5, u"NotApplicable"),
	}
PostStates = (
	(1, u"Waiting"),
	(2, u"Forfeited"), 
	(3, u"Current"),
	(4, u"Processed"), 
	)

lookup = lambda tuple, selection: {key: val for key, val in tuple}[selection]

class Category(models.Model):
	parent = models.ForeignKey('Category', blank = True, null = True) 
	name = models.CharField(max_length=128)
	def __unicode__(self):
		return u"Category: {0} ({1})".format(self.name, self.parent)


class Initiative(models.Model):
	name = models.CharField(max_length=128)
	category = models.ForeignKey(Category)
	text = models.TextField()
	admin_text = models.TextField(blank=True)
	def __unicode__(self):
		return u"Initiative: {0}".format(self.name)

class Suggestion(models.Model):
	name = models.CharField(max_length=128)
	initiative = models.ForeignKey(Initiative)
	text = models.TextField()
	admin_text = models.TextField(blank=True)
	#round = models.IntegerField(default = 0)
	def __unicode__(self):
		return u"Suggestion: {0} [{1}({2}]".format(self.name, self.initiative, self.initiative.category)

class Voter(models.Model):
	user = models.ForeignKey(User)
	weight = models.IntegerField(default = 1)
	def __unicode__(self):
		return u"Voter: {0} ({1})".format(self.user, self.weight)

	
class SuggestionParticipation(models.Model):
	suggestion = models.ForeignKey(Suggestion)
	round = models.IntegerField(default = 0)
	def __unicode__(self):
		return u"SuggestionParticipation: {0} ({1})".format(self.suggestion, self.round)

class Vote(models.Model):
	voter = models.ForeignKey(Voter)
	alternative = models.ForeignKey(SuggestionParticipation, related_name="votes")
	#FIXME: Make save model-function requiring either above or below
	above = models.ForeignKey(SuggestionParticipation, null = True, blank = True, related_name="inferiours")
	below = models.ForeignKey(SuggestionParticipation, null = True, blank = True, related_name="superiors")
	priority = models.IntegerField(default = 0)
	def __unicode__(self):
		return u"Vote: {0} ({1})".format(self.voter, self.alternative)

class InitiativeDelegation(models.Model):
	delegator = models.ForeignKey(User, related_name="initiative_delegators")
	delegate = models.ForeignKey(User, related_name="initiative_delegates")
	target = models.ForeignKey(Initiative, related_name="direct_delegations")
	def __unicode__(self):
		return u"IDelegation: {0} from {1} to {2}".format(self.target, self.delegator, self.delegate)

class CategoryDelegation(models.Model):
	delegator = models.ForeignKey(User, related_name="category_delegators")
	delegate = models.ForeignKey(User, related_name="category_delegates")
	target = models.ForeignKey(Category, related_name="category_delegations")
	def __unicode__(self):
		return u"CDelegation: {0} from {1} to {2}".format(self.target, self.delegator, self.delegate)
