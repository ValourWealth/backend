# admin.py
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, UserProfiles, CourseEnrollment, ChallengeParticipant, Challenge, MT5Snapshot, SectorExposure
class UserAdmin(BaseUserAdmin):
    model = User
    list_display = ('id', 'username', 'email', 'first_name', 'last_name', 'is_staff', 'is_active', 'created_at')
    list_filter = ('is_staff', 'is_active', 'created_at')
    search_fields = ('username', 'email', 'first_name', 'last_name')
    ordering = ('-created_at',)

    fieldsets = (
        (None, {'fields': ('username', 'email', 'password')}),
        ('Personal Info', {'fields': ('first_name', 'last_name')}),
        ('Permissions', {'fields': ('is_staff', 'is_active', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important Dates', {'fields': ('last_login', 'date_joined')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'password1', 'password2', 'is_staff', 'is_active')}
        ),
    )

admin.site.register(User, UserAdmin)


from django.contrib import admin
from django.utils.html import format_html
from .models import UserProfiles

class UserProfileAdmin(admin.ModelAdmin):
    list_display = (
        'user',
        'phone_number',
        'country',
        'state',
        'role',
        'subscription_status',  # 👈 Add this
        'profile_image_preview',
        'profile_image_url',   
        'updated_at',
    )
    readonly_fields = ('profile_image_preview', 'profile_image_url', 'updated_at')
    search_fields = ('user__username', 'phone_number', 'country', 'state')
    autocomplete_fields = ['user']
    list_filter = ['role', 'subscription_status']  # 👈 Optional: make it filterable

    def profile_image_preview(self, obj):
        if obj.profile_photo:
            return format_html(
                '<img src="https://pub-552c13ad8f084b0ca3d7b5aa8ddb03a7.r2.dev/{}" width="60" height="60" style="object-fit:cover;border-radius:50%;" />',
                obj.profile_photo.name
            )
        return "No Image"
    profile_image_preview.short_description = 'Profile Photo'

    def profile_image_url(self, obj):
        if obj.profile_photo:
            return format_html(
                '<a href="https://pub-552c13ad8f084b0ca3d7b5aa8ddb03a7.r2.dev/{}" target="_blank">View URL</a>',
                obj.profile_photo.name
            )
        return "Not uploaded"
    profile_image_url.short_description = 'Public URL'

    fieldsets = (
        (None, {
            'fields': (
                'user',
                'bio',
                'phone_number',
                'country',
                'state',
                'role',
                'subscription_status', 
                'profile_photo'
            )
        }),
        ('Advanced options', {
            'classes': ('collapse',),
            'fields': ('updated_at',)
        }),
    )


admin.site.register(UserProfiles, UserProfileAdmin)

from django.contrib import admin
from .models import UserProfiles

from django.contrib import admin
from .models import Course, CourseLevel, Video, Note


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ['title', 'user', 'created_at']
    search_fields = ['title', 'description']

@admin.register(CourseLevel)
class CourseLevelAdmin(admin.ModelAdmin):
    list_display = ['course', 'level']
    list_filter = ['level']

from django.contrib import admin
from .models import Video
from django.utils.html import format_html

@admin.register(Video)
class VideoAdmin(admin.ModelAdmin):
    list_display = ("title", "course_level", "uploaded_at", "thumb_preview", "public_url_link")
    readonly_fields = ("uploaded_at", "public_url_link", "thumb_preview")
    fields = (
        "title", "course_level",
        "video_file", "manual_video_url",
        "thumbnail_url",        # plain text input
        "uploaded_at", "public_url_link", "thumb_preview",
    )

    def public_url_link(self, obj):
        return format_html('<a href="{0}" target="_blank">{0}</a>', obj.public_url)
    public_url_link.short_description = "Public URL"

    def thumb_preview(self, obj):
        if obj.thumbnail_url:
            return format_html(
                '<a href="{0}" target="_blank"><img src="{0}" style="height:70px;border-radius:6px;" /></a>',
                obj.thumbnail_url,
            )
        return "—"
    thumb_preview.short_description = "Thumbnail"



@admin.register(Note)
class NoteAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'course_level', 'created_at')
    search_fields = ('title',)
    list_filter = ('course_level__level', 'created_at')




from django.contrib import admin
from .models import MCQQuestion

@admin.register(MCQQuestion)
class MCQQuestionAdmin(admin.ModelAdmin):
    list_display = ('question', 'course_level', 'correct_answer')
    search_fields = ('question',)
    list_filter = ('course_level',)



@admin.register(CourseEnrollment)
class CourseEnrollmentAdmin(admin.ModelAdmin):
    list_display = ('user', 'course', 'enrolled_at')
    search_fields = ('user__username', 'course__title')
    list_filter = ('enrolled_at',)
    
# =================================================================================================================================================
    
from django.contrib import admin
from .models import TradeJournalEntry

@admin.register(TradeJournalEntry)
class TradeJournalEntryAdmin(admin.ModelAdmin):
    list_display = (
        'user',
        'symbol',
        'trade_type',
        'entry_date',
        'exit_date',
        'entry_price',
        'exit_price',
        'position_size',
        'created_at',
    )
    list_filter = ('trade_type', 'entry_date', 'exit_date', 'user')
    search_fields = ('symbol', 'user__username', 'entry_reason', 'exit_reason')
    readonly_fields = ('created_at',)

    fieldsets = (
        ('Basic Trade Info', {
            'fields': ('user', 'symbol', 'trade_type', 'entry_date', 'entry_price', 'exit_date', 'exit_price', 'position_size')
        }),
        ('Risk Management', {
            'fields': ('risk_reward_ratio', 'stop_loss', 'take_profit')
        }),
        ('Analysis & Notes', {
            'fields': ('entry_reason', 'exit_reason', 'emotional_state', 'market_conditions',
                       'what_went_well', 'what_went_wrong', 'lessons_learned', 'additional_notes')
        }),
        ('Metadata', {
            'fields': ('created_at',),
        }),
    )




    
from .models import Webinar
from django.contrib import admin
from django.utils.html import format_html

@admin.register(Webinar)
class WebinarAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "presenter",
        "date",
        "time",
        "level",
        "status",
        "thumbnail_preview",     # 👈 Custom column
        "thumbnail_url",         # 👈 Custom column
    )
    list_filter = ("status", "level")
    search_fields = ("title", "presenter")
    readonly_fields = ("created_at", "thumbnail_preview", "thumbnail_url")

    def thumbnail_preview(self, obj):
        if obj.thumbnail:
            return format_html(
                '<img src="https://pub-552c13ad8f084b0ca3d7b5aa8ddb03a7.r2.dev/{}" width="100" height="60" style="object-fit:cover;border-radius:4px;" />',
                obj.thumbnail.name
            )
        return "No Thumbnail"
    thumbnail_preview.short_description = "Thumbnail Preview"

    def thumbnail_url(self, obj):
        if obj.thumbnail:
            return format_html(
                '<a href="https://pub-552c13ad8f084b0ca3d7b5aa8ddb03a7.r2.dev/{}" target="_blank">View Thumbnail</a>',
                obj.thumbnail.name
            )
        return "Not Uploaded"
    thumbnail_url.short_description = "Thumbnail URL"

    fieldsets = (
        (None, {
            'fields': (
                "title",
                "description",
                "presenter",
                "thumbnail",     
                "thumbnail_preview",
                "thumbnail_url",
                "recording_link",
                "date",
                "time",
                "duration",
                "level",
                "status",
                "registered_users",
            )
        }),
        ("Timestamps", {
            'classes': ("collapse",),
            'fields': ("created_at",),
        }),
    )


from django.contrib import admin
from .models import CallCredit, Session

@admin.register(CallCredit)
class CallCreditAdmin(admin.ModelAdmin):
    list_display = ('user', 'hours_remaining')
    search_fields = ('user__username',)
    list_filter = ('hours_remaining',)
    ordering = ('user',)

@admin.register(Session)
class SessionAdmin(admin.ModelAdmin):
    list_display = ('user', 'analyst', 'date', 'time_slot', 'status', 'created_at')
    search_fields = ('user__username', 'analyst__username')
    list_filter = ('status', 'date')
    ordering = ('-date', '-time_slot')

from .models import FeatureRequest, Vote 

admin.site.register(Vote)
admin.site.register(FeatureRequest)
# admin.site.register(Portfolio)
# admin.site.register(PortfolioAsset)
admin.site.register(Challenge)
admin.site.register(ChallengeParticipant)


# =================================================================================================================================================
from django.contrib import admin
from .models import Conversation, Message
from django.utils.html import format_html


class MessageInline(admin.TabularInline):
    model = Message
    extra = 1  # Allows adding new messages directly
    fields = ['sender', 'content', 'timestamp']
    readonly_fields = ['timestamp']
    show_change_link = False


class ConversationAdmin(admin.ModelAdmin):
    list_display = ['id', 'participant_usernames', 'created_at']
    inlines = [MessageInline]
    search_fields = ['participants__username']

    def participant_usernames(self, obj):
        return ", ".join([user.username for user in obj.participants.all()])
    participant_usernames.short_description = "Participants"


class MessageAdmin(admin.ModelAdmin):
    list_display = ['id', 'conversation', 'sender', 'short_content', 'timestamp']
    list_filter = ['sender']
    search_fields = ['content', 'sender__username']
    readonly_fields = ['timestamp']

    def short_content(self, obj):
        return (obj.content[:50] + '...') if len(obj.content) > 50 else obj.content
    short_content.short_description = "Message"


admin.site.register(Conversation, ConversationAdmin)
admin.site.register(Message, MessageAdmin)
from . models import AnalystChat, AnalystMessage
admin.site.register(AnalystMessage)
admin.site.register(AnalystChat)
admin.site.register(MT5Snapshot)
admin.site.register(SectorExposure)

# =================================================================================================================================================
from django.utils.safestring import mark_safe

from django.contrib import admin
from .models import Course, CourseLevel, Video, Note, MCQQuestion, VideoProgress, CourseEnrollment, LevelProgress

@admin.register(LevelProgress)
class LevelProgressAdmin(admin.ModelAdmin):
    list_display = ('user', 'course_level', 'passed_quiz')
    list_filter = ('passed_quiz', 'course_level__level')
    search_fields = ('user__username',)


# Beginer hub management system:
from django.contrib import admin
from .models import BeginnerHubCourse, BeginnerHubVideo


class BeginnerHubVideoInline(admin.TabularInline):
    model = BeginnerHubVideo
    extra = 1


class BeginnerHubCourseAdmin(admin.ModelAdmin):
    list_display = ['title', 'category']
    inlines = [BeginnerHubVideoInline]


admin.site.register(BeginnerHubCourse, BeginnerHubCourseAdmin)
admin.site.register(BeginnerHubVideo)


from django.contrib import admin
from .models import WeeklyBriefing, TradeIdea

from django.contrib import admin
from django.utils.html import format_html
from .models import WeeklyBriefing, TradeIdea

class TradeIdeaInline(admin.TabularInline):
    model = TradeIdea
    extra = 1
    fields = ('ticker', 'target_price', 'stop_loss', 'timeframe', 'direction')


@admin.register(WeeklyBriefing)
class WeeklyBriefingAdmin(admin.ModelAdmin):
    list_display = (
        'title', 'published_date', 'duration', 'analyst_name', 
        'is_platinum_only', 'thumbnail_preview', 'thumbnail_url', 'get_public_url'
    )
    list_filter = ('published_date', 'is_platinum_only')
    search_fields = ('title', 'analyst_name')
    inlines = [TradeIdeaInline]
    readonly_fields = ('published_date', 'thumbnail_preview', 'thumbnail_url')

    fieldsets = (
        (None, {
            'fields': (
                'title', 'video_url', 'manual_video_url', 'published_date', 'duration',
                'analyst_name', 'analyst_title',
                'summary', 'key_points', 'is_platinum_only',
                'thumbnail', 'thumbnail_preview', 'thumbnail_url'
            )
        }),
    )

    def get_public_url(self, obj):
        return obj.public_url
    get_public_url.short_description = "Public URL"

    def thumbnail_preview(self, obj):
        if obj.thumbnail:
            return format_html(
                '<img src="https://pub-552c13ad8f084b0ca3d7b5aa8ddb03a7.r2.dev/{}" width="100" height="60" style="object-fit:cover;border-radius:4px;" />',
                obj.thumbnail.name
            )
        return "No Image"
    thumbnail_preview.short_description = "Thumbnail"

    def thumbnail_url(self, obj):
        if obj.thumbnail:
            return format_html(
                '<a href="https://pub-552c13ad8f084b0ca3d7b5aa8ddb03a7.r2.dev/{}" target="_blank">View URL</a>',
                obj.thumbnail.name
            )
        return "Not uploaded"
    thumbnail_url.short_description = "Thumbnail URL"
    
    
    
@admin.register(TradeIdea)
class TradeIdeaAdmin(admin.ModelAdmin):
    list_display = ('ticker', 'briefing', 'direction', 'target_price', 'stop_loss', 'timeframe')
    list_filter = ('direction',)
    search_fields = ('ticker', 'briefing__title')




from django.contrib import admin
from .models import EditorsChoice

@admin.register(EditorsChoice)
class EditorsChoiceAdmin(admin.ModelAdmin):
    list_display = ['title', 'category', 'created_at']
    search_fields = ['title', 'category']
    list_filter = ['category']
    prepopulated_fields = {"slug": ("title",)}
