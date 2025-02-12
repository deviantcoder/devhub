from django.contrib import admin
from .models import *


admin.site.register(Project)
admin.site.register(ProjectMedia)
admin.site.register(Feature)


@admin.register(ProjectStats)
class ProjectStatsAdmin(admin.ModelAdmin):
    list_display = ['project', 'upvotes', 'downvotes', 'votes_ratio']

    def votes_ratio(self, object):
        return object.get_votes_ratio


admin.site.register(ProjectVote)
