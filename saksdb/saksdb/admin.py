from django.contrib import admin
from saksdb.models import  Category, Initiative, Suggestion, Voter, SuggestionParticipation, Vote, InitiativeDelegation, CategoryDelegation

admin.site.register(Category)
admin.site.register(Initiative)
admin.site.register(Suggestion)
admin.site.register(Voter)
admin.site.register(SuggestionParticipation)
admin.site.register(Vote)
admin.site.register(InitiativeDelegation)
admin.site.register(CategoryDelegation)
