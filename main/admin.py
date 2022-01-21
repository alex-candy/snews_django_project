from django.contrib import admin
from .models import *

# class ArticlesAdmin(admin.ModelAdmin):
#     search_fields = ('title',)
#     prepopulated_fields = {"slug":("title",)}
#
# class VideoAdmin(admin.ModelAdmin):
#     search_fields = ('title',)
#     prepopulated_fields = {"slug":("title",)}




admin.site.register(Articles)
admin.site.register(Coment)
admin.site.register(Category)
admin.site.register(Video)
admin.site.register(Condition)
admin.site.register(Placing)
admin.site.register(Source)
admin.site.register(TypeVideo)
# admin.site.register(Articles, ArticlesAdmin)
# admin.site.register(KriminalNow, KriminalAdmin)
# admin.site.register(KulturNow, KulturAdmin)
# admin.site.register(NaukNow, NaukAdmin)
# admin.site.register(Navig)
# admin.site.register(Registration)
# admin.site.register(Nowost)
# admin.site.register(Sotrud)
# admin.site.register(PolitikNow, PolitikAdmin)
# admin.site.register(SportNow, SportAdmin)





 # Register your models here.
