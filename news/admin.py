from django.contrib import admin

from news.models import *

# Register your models here.
class DeepArchiveAdmin(admin.ModelAdmin):
    list_display = ('id', 'org', 'word', 'count','date')
    
class BoneBrothArchiveAdmin(admin.ModelAdmin):
    list_display = ('id', 'org', 'word', 'count','date')


class EntryBlacklist(admin.ModelAdmin):
    list_display = ('id', 'word')

class EntryWhitelist(admin.ModelAdmin):
    list_display = ('id', 'word')

class TopWordsAdmin(admin.ModelAdmin):
    list_display = ('id', 'word', 'date')
    
class TopWordsByOrgAdmin(admin.ModelAdmin):
    list_display = ('id', 'word', 'org','date')

class MillionsAdmin(admin.ModelAdmin):
    list_display = ('id', 'headline', 'date')
    
class ThirtyThreesAdmin(admin.ModelAdmin):
    list_display = ('id', 'headline', 'date')


admin.site.register(BoneBrothArchive, BoneBrothArchiveAdmin)
admin.site.register(DeepArchive, DeepArchiveAdmin)
admin.site.register(TopWords, TopWordsAdmin)
admin.site.register(TopWordsByOrg, TopWordsByOrgAdmin)
admin.site.register(Whitelist, EntryWhitelist)
admin.site.register(Blacklist, EntryBlacklist)
admin.site.register(Millions, MillionsAdmin)
admin.site.register(ThirtyThrees, ThirtyThreesAdmin)

