from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
from django_countries.fields import CountryField
from django.db import models
from django.contrib.auth import get_user_model
from django.conf import settings
from VWBE.storage_backends import R2Storage
from django.db import models
from django.conf import settings





class User(AbstractUser):
    # Fields inherited: id, username, first_name, last_name, email, password, etc.
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.username
# =========================================================================================================

# user:::::=================
# lan.M
# Vwlogin1

# asdfing
# qwerty1234

# Ricky.K 
# KM8z:pH64T8wiQK

# Amara.D 
# fiuSC4waM8!.N4J

# Manuel.S
# XnSwuUW-wHufNf4

# valourwealth
# FKRxteszZGXynV61
# ===========================

SUBSCRIPTION_CHOICES = [
    ('free', 'Free'),
    ('premium', 'Premium'),
    ('platinum', 'Platinum'),
]


class UserProfiles(models.Model):
    USER_ROLES = [
        ('admin', 'Admin'),
        ('analyst', 'Analyst'),
        ('user', 'User'),
    ]
    
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='profile')
    bio = models.TextField(blank=True, null=True)
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    profile_photo = models.ImageField(
        upload_to='profile_photos/',
        storage=R2Storage(),  # upload to R2
        blank=True,
        null=True
    )
    subscription_status = models.CharField(max_length=20, choices=SUBSCRIPTION_CHOICES, default='free')
    country = CountryField(blank=True, null=True)
    state = models.CharField(max_length=100, blank=True, null=True)  # Optional: dynamic on frontend
    role = models.CharField(max_length=20, choices=USER_ROLES, default='user')  # New field for role
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username}'s Profile"

    @property
    def profile_photo_public_url(self):
        if self.profile_photo:
            # return f"https://pub-552c13ad8f084b0ca3d7b5aa8ddb03a7.r2.dev/{self.profile_photo.name}"
            return f"https://pub-552c13ad8f084b0ca3d7b5aa8ddb03a7.r2.dev/{self.profile_photo.name}"





from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class LevelChoices(models.TextChoices):
    BEGINNER = 'Beginner', 'Beginner'
    INTERMEDIATE = 'Intermediate', 'Intermediate'
    PROFESSIONAL = 'Professional', 'Professional'


class Course(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='courses')
    title = models.CharField(max_length=255)
    description = models.TextField()
    thumbnail = models.ImageField(upload_to='course_thumbnails/')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class CourseLevel(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='levels')
    level = models.CharField(max_length=20, choices=LevelChoices.choices)
    
    class Meta:
        unique_together = ('course', 'level')  # Prevent duplicate levels per course

    def __str__(self):
        return f"{self.course.title} - {self.level}"


class Video(models.Model):
    course_level = models.ForeignKey(CourseLevel, on_delete=models.CASCADE, related_name='videos')
    title = models.CharField(max_length=255)
    video_file = models.FileField(
        storage=R2Storage(),
        upload_to='course_videos/',
        null=True,
        blank=True
    )
      #  store a plain URL, not a file
    thumbnail_url = models.URLField(null=True, blank=True)
    manual_video_url = models.URLField(null=True, blank=True)  #  Paste R2 public URL here
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} - {self.course_level.level}"

    @property
    def public_url(self):
        if self.video_file and getattr(self.video_file, 'name', '').strip() != '':
            file_name = self.video_file.name.strip()
            if file_name.startswith("http://") or file_name.startswith("https://"):
                return file_name
            return f"https://pub-552c13ad8f084b0ca3d7b5aa8ddb03a7.r2.dev/{file_name}"
        elif self.manual_video_url:
            return self.manual_video_url
        return None
    
    
# for video progress 
class VideoProgress(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    video = models.ForeignKey(Video, on_delete=models.CASCADE)
    watched = models.BooleanField(default=False)
    watched_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'video')

# this is for the whole user progress of the courses 
# models.py
class CourseEnrollment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="enrollments")
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name="enrollments")
    enrolled_at = models.DateTimeField(auto_now_add=True)




class Note(models.Model):
    course_level = models.ForeignKey(CourseLevel, on_delete=models.CASCADE, related_name='notes')
    title = models.CharField(max_length=255)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} - {self.course_level.level}"


class MCQQuestion(models.Model):
    course_level = models.ForeignKey(CourseLevel, on_delete=models.CASCADE, related_name="mcq_questions")
    question = models.TextField()
    option_a = models.CharField(max_length=255)
    option_b = models.CharField(max_length=255)
    option_c = models.CharField(max_length=255)
    option_d = models.CharField(max_length=255)
    correct_answer = models.CharField(max_length=1, choices=[('A', 'A'), ('B', 'B'), ('C', 'C'), ('D', 'D')])


class LevelProgress(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    course_level = models.ForeignKey(CourseLevel, on_delete=models.CASCADE)
    passed_quiz = models.BooleanField(default=False)
    passed_at = models.DateTimeField(auto_now_add=True)
    quiz_score = models.FloatField(null=True, blank=True)  
    
    class Meta:
        unique_together = ('user', 'course_level')
        
    def __str__(self):
        return f"{self.user.username} - {self.course_level.level} - {'Passed' if self.passed_quiz else 'Not Passed'}"





# ********************************************************************************************************************************************************************************
# **************************************************Platinum member****************************************************************************************************************************************************
# For platinum member journal Trade notes:
class TradeJournalEntry(models.Model):
    TRADE_TYPES = [
        ('long', 'Long'),
        ('short', 'Short'),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='journal_entries')

    symbol = models.CharField(max_length=50)
    trade_type = models.CharField(max_length=10, choices=TRADE_TYPES)
    entry_date = models.DateField()
    entry_price = models.DecimalField(max_digits=12, decimal_places=4)
    exit_date = models.DateField()
    exit_price = models.DecimalField(max_digits=12, decimal_places=4)
    position_size = models.PositiveIntegerField()
    risk_reward_ratio = models.CharField(max_length=20, blank=True)
    stop_loss = models.DecimalField(max_digits=12, decimal_places=4, null=True, blank=True)
    take_profit = models.DecimalField(max_digits=12, decimal_places=4, null=True, blank=True)

    entry_reason = models.TextField()
    exit_reason = models.TextField()
    emotional_state = models.TextField(blank=True)
    market_conditions = models.TextField(blank=True)

    what_went_well = models.TextField(blank=True)
    what_went_wrong = models.TextField(blank=True)
    lessons_learned = models.TextField()
    additional_notes = models.TextField(blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.symbol} - {self.user.username}"


from django.db import models
from django.conf import settings

class Webinar(models.Model):
    STATUS_CHOICES = [
        ("Upcoming", "Upcoming"),
        ("Ongoing", "Ongoing"),
        ("Outdated", "Outdated"),
    ]

    LEVEL_CHOICES = [
        ("Beginner", "Beginner"),
        ("Intermediate", "Intermediate"),
        ("Advanced", "Advanced"),
    ]

    title = models.CharField(max_length=255)
    description = models.TextField()
    presenter = models.CharField(max_length=255)
    recording_link = models.URLField(blank=True, null=True)
    date = models.DateField()
    time = models.TimeField()
    duration = models.CharField(max_length=50)
    level = models.CharField(max_length=20, choices=LEVEL_CHOICES)
    registered_users = models.ManyToManyField(User, related_name="registered_webinars", blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="Upcoming")
    created_at = models.DateTimeField(auto_now_add=True)
    thumbnail = models.ImageField(
        upload_to='webinar-thumbnails/',
        storage=R2Storage(), 
        blank=True,
        null=True
    )


    def __str__(self):
        return self.title
    
    @property
    def thumbnail_public_url(self):
        if self.thumbnail:
            return f"https://pub-552c13ad8f084b0ca3d7b5aa8ddb03a7.r2.dev/{self.thumbnail.name}"
        return None

    def registered_count(self):
        return self.registered_users.count()
    
    
# This is the group chat of the all paltinum member with analyst
from django.contrib.auth import get_user_model
from django.db import models
User = get_user_model()

class Conversation(models.Model):
    participants = models.ManyToManyField(User)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Conversation {self.id} - {', '.join([p.username for p in self.participants.all()])}"

class Message(models.Model):
    conversation = models.ForeignKey(Conversation, related_name='messages', on_delete=models.CASCADE)
    sender = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)
    is_notification = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.sender.username} - {self.timestamp.strftime('%Y-%m-%d %H:%M')}"
    
    
# this is for one to one chat with analyst and platinum member 
from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class AnalystChat(models.Model):
    user = models.ForeignKey(User, related_name="analyst_chats", on_delete=models.CASCADE)
    analyst = models.ForeignKey(User, related_name="assigned_chats", on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

class AnalystMessage(models.Model):
    chat = models.ForeignKey(AnalystChat, related_name="messages", on_delete=models.CASCADE)
    sender = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.sender.username}: {self.content[:20]}"

    

# =========================================================================================================
# for scheduling calling with analyst
from django.db import models
from django.conf import settings

class CallCredit(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='call_credit')
    hours_remaining = models.IntegerField(default=10)  # 10 free hours initially

    def __str__(self):
        return f"{self.user.email} - {self.hours_remaining} hours remaining"


class Session(models.Model):
    STATUS_CHOICES = [
        ("Confirmed", "Confirmed"),
        ("Cancelled", "Cancelled"),
        ("Completed", "Completed"),
        ("Rescheduled", "Rescheduled"),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='sessions')
    analyst = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='analyzed_sessions')
    date = models.DateField()
    time_slot = models.TimeField()
    duration = models.IntegerField(default=60)  # minutes
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="Confirmed")
    notes = models.TextField(blank=True, null=True)  # 🆕 User apne notes yahan likhega/update karega
    notes_pdf = models.FileField(upload_to='session_notes/', blank=True, null=True)
    recording_link = models.URLField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Session: {self.user.email} with {self.analyst.email} on {self.date} at {self.time_slot}"

# =========================================================================================================
from django.db import models
from django.conf import settings

User = get_user_model()

class FeatureRequest(models.Model):
    STATUS_CHOICES = [
        ("Voting Open", "Voting Open"),
        ("Closed", "Closed"),
    ]

    title = models.CharField(max_length=255)
    description = models.TextField()
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name="feature_requests")
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default="Voting Open")
    votes_needed = models.IntegerField(default=200)
    deadline = models.DateTimeField()  # Voting end date

    def votes_count(self):
        return self.votes.count()

    def __str__(self):
        return self.title

class Vote(models.Model):
    feature = models.ForeignKey(FeatureRequest, on_delete=models.CASCADE, related_name="votes")
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    voted_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('feature', 'user')  # ❗ same user can't vote twice


# =========================================================================================================
# portfolio, challenges, leaderboard
# models.py
from django.db import models
from django.conf import settings
from django_countries.fields import CountryField

User = get_user_model()

# Portfolio and Assets
class Portfolio(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='portfolio')
    total_value = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    total_gain_loss = models.DecimalField(max_digits=15, decimal_places=2, default=0)  # daily/weekly change
    total_gain_loss_percent = models.DecimalField(max_digits=6, decimal_places=2, default=0)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def update_total_value(self):
        assets = self.assets.all()
        self.total_value = sum(asset.value for asset in assets)
        self.save()

    def __str__(self):
        return f"{self.user.username}'s Portfolio"

class PortfolioAsset(models.Model):
    ASSET_TYPES = (
        ('stocks', 'Stocks'),
        ('crypto', 'Crypto'),
        ('forex', 'Forex'),
        ('commodities', 'Commodities'),
    )

    portfolio = models.ForeignKey(Portfolio, on_delete=models.CASCADE, related_name='assets')
    asset_type = models.CharField(max_length=20, choices=ASSET_TYPES)
    value = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    percentage = models.DecimalField(max_digits=5, decimal_places=2, default=0)

    def __str__(self):
        return f"{self.portfolio} - {self.asset_type}"

from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Challenge(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    start_date = models.DateField()
    end_date = models.DateField()
    questions = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    participants_count = models.IntegerField(default=0)

    def __str__(self):
        return self.title


class ChallengeParticipant(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='challenge_participants')
    challenge = models.ForeignKey(Challenge, on_delete=models.CASCADE, related_name='participants')
    
    answers = models.TextField(null=True, blank=True)
    screenshots = models.FileField(storage=R2Storage(), upload_to='challenge_screenshots/', blank=True, null=True)
    
    leaderboard_position = models.IntegerField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'challenge')

    def __str__(self):
        return f"{self.user.username} in {self.challenge.title}"

    @property
    def screenshot_public_url(self):
        if self.screenshots:
            return f"https://pub-552c13ad8f084b0ca3d7b5aa8ddb03a7.r2.dev/{self.screenshots.name}"
        return None

# Landing page Blogs
from django.db import models
from django.utils.text import slugify
from django.contrib.auth import get_user_model
from VWBE.storage_backends import R2Storage  # if you're using Cloudflare R2 for media

User = get_user_model()

class EditorsChoice(models.Model):
    CATEGORY_CHOICES = [
        ('Markets', 'Markets'),
        ('Crypto', 'Crypto'),
        ('Forex', 'Forex'),
        ('Stocks', 'Stocks'),
    ]

    title = models.CharField(max_length=255)
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES, default='Markets')
    description = models.TextField()
    image = models.FileField(upload_to='editor_choices/', storage=R2Storage())
    slug = models.SlugField(max_length=255, unique=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title[:200])
        super().save(*args, **kwargs)

    @property
    def image_url(self):
        return f"https://pub-552c13ad8f084b0ca3d7b5aa8ddb03a7.r2.dev/{self.image.name}"
    def __str__(self):
        return self.title











#========================== Weekly briefing for platinum members ============================================================
from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone

class WeeklyBriefing(models.Model):
    title = models.CharField(max_length=255)
    video_url = models.URLField()  # YouTube, Vimeo, or Cloudflare stream link
    published_date = models.DateField(default=timezone.now)
    duration = models.CharField(max_length=10)  # e.g., "28:23"
    analyst_name = models.CharField(max_length=100)
    analyst_title = models.CharField(max_length=100)
    summary = models.TextField()
    key_points = models.JSONField()  # List of strings
    is_platinum_only = models.BooleanField(default=True)
    manual_video_url = models.URLField(null=True, blank=True)
    thumbnail = models.ImageField(
        upload_to='weekly_thumbnails/',
        storage=R2Storage(),  # Uploads to R2 like profile photos
        blank=True,
        null=True
    )

    def __str__(self):
        return self.title
    
    @property
    def public_url(self):
        return self.manual_video_url or self.video_url
    
    @property
    def thumbnail_public_url(self):
        if self.thumbnail:
            return f"https://pub-552c13ad8f084b0ca3d7b5aa8ddb03a7.r2.dev/{self.thumbnail.name}"
        return None
    
    


from decimal import Decimal, ROUND_HALF_UP
from django.core.exceptions import ValidationError

class TradeIdea(models.Model):
    briefing = models.ForeignKey(WeeklyBriefing, on_delete=models.CASCADE, related_name='trade_ideas')
    ticker = models.CharField(max_length=10)
    target_price = models.DecimalField(max_digits=10, decimal_places=2)
    stop_loss = models.DecimalField(max_digits=10, decimal_places=2)
    timeframe = models.CharField(max_length=100)
    direction = models.CharField(max_length=10, choices=[("LONG", "Long"), ("SHORT", "Short")])

    def __str__(self):
        return f"{self.ticker} - {self.direction}"

    def clean(self):
        # Round to 2 decimal places manually (safe from extra input)
        self.target_price = Decimal(self.target_price).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
        self.stop_loss = Decimal(self.stop_loss).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)




# =====================================================================================================================================================
# ======For notification and chat message and admin panel notification to platinum member =====================================================



from django.contrib.auth import get_user_model

User = get_user_model()

class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')
    title = models.CharField(max_length=255)
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.title}"




    
# ********************************************************************************************************************************************************************************
# *********************************************************************************************************************************************************************************



# Beginner Hub course management system:
# beginnerhub/models.py

class BeginnerHubCourse(models.Model):
    CATEGORY_CHOICES = [('Stock', 'Stock'), ('Forex', 'Forex'), ('Crypto', 'Crypto')]

    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)

    def __str__(self):
        return self.title



class BeginnerHubVideo(models.Model):
    course = models.ForeignKey(BeginnerHubCourse, on_delete=models.CASCADE, related_name="videos", null=True, blank=True)

    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)

    video_file = models.FileField(storage=R2Storage(), upload_to='beginnerhub_videos/', null=True, blank=True)
    manual_video_url = models.URLField(null=True, blank=True)

    thumbnail_file = models.ImageField(storage=R2Storage(), upload_to='beginnerhub_thumbnails/', null=True, blank=True)
    manual_thumbnail_url = models.URLField(null=True, blank=True)

    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.course.title}: {self.title}"

    @property
    def video_url(self):
        if self.video_file and getattr(self.video_file, 'name', '').strip():
            name = self.video_file.name.replace("valourswealth/", "")
            return f"https://pub-552c13ad8f084b0ca3d7b5aa8ddb03a7.r2.dev/{name}"
        elif self.manual_video_url:
            return self.manual_video_url
        return None

    @property
    def thumbnail_url(self):
        if self.thumbnail_file and getattr(self.thumbnail_file, 'name', '').strip():
            name = self.thumbnail_file.name.replace("valourswealth/", "")
            return f"https://pub-552c13ad8f084b0ca3d7b5aa8ddb03a7.r2.dev/{name}"
        elif self.manual_thumbnail_url:
            return self.manual_thumbnail_url
        return None

    
    


# =========================================================================================================

# Contact form for wealth series
class SalesInquiry(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    inquiry_type = models.CharField(max_length=100, blank=True)
    submitted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.inquiry_type}"





# ======================================================================= Meta Trader 5 for platinum portfolio
from django.conf import settings
from django.db import models

class MT5Snapshot(models.Model):
    user = models.ForeignKey(
    settings.AUTH_USER_MODEL,
    on_delete=models.CASCADE,
    related_name="mt5_snapshots",
    null=True,  # <- temporarily allow nulls
    blank=True  )
    timestamp = models.DateTimeField(auto_now_add=True)
    account_login = models.CharField(max_length=50)
    balance = models.FloatField()
    equity = models.FloatField()
    assets = models.JSONField(default=list)
    margin = models.FloatField()
    leverage = models.IntegerField()
    portfolio_value = models.FloatField(default=0)
    open_positions = models.JSONField()
    recent_trades = models.JSONField()
    free_margin = models.FloatField(default=0)
    market_watch = models.JSONField(default=list)



class SectorExposure(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    data = models.JSONField(default=list)
    updated_at = models.DateTimeField(auto_now=True)