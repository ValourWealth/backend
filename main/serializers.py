from rest_framework import serializers
from .models import Course, CourseLevel, Video, Note, User, MCQQuestion, UserProfiles, CourseEnrollment
from django.contrib.auth import get_user_model
from django.urls import path
from .models import *
from rest_framework import serializers, generics, permissions
from .models import TradeJournalEntry

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "id",
            "username",
            "email",
            "first_name",
            "last_name",
            "created_at",
            "password"
        ]
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user

class NFTBadgeSerializer(serializers.ModelSerializer):
    image_url = serializers.SerializerMethodField()

    class Meta:
        model = NFTBadge
        fields = ['id', 'name', 'category', 'image_url', 'description', 'manually_assignable',
                  'linked_user', 'linked_challenge', 'assigned_at']

    def get_image_url(self, obj):
        return obj.image_public_url



class UserProfileSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username', required=False)
    first_name = serializers.CharField(source='user.first_name', required=False)
    subscription_status = serializers.CharField(read_only=True)
    last_name = serializers.CharField(source='user.last_name', required=False)
    email = serializers.EmailField(source='user.email', read_only=True)
    password = serializers.CharField(write_only=True, required=False)
    is_staff = serializers.BooleanField(source='user.is_staff', read_only=True)
    is_superuser = serializers.BooleanField(source='user.is_superuser', read_only=True)
    profile_photo = serializers.ImageField(required=False)
    profile_photo_url = serializers.SerializerMethodField()
    primary_badge = NFTBadgeSerializer(read_only=True)
    role = serializers.ChoiceField(choices=UserProfiles.USER_ROLES, required=False)  # Add the role field

    class Meta:
        model = UserProfiles
        fields = [
            'username',
            'first_name',
            'last_name',
            'email',
            'password',
            'phone_number',
            'country',
            'state',
            'profile_photo',
            'profile_photo_url',
            'updated_at',
            'subscription_status',
            'is_staff',
            'is_superuser',
             'primary_badge',
            'role',  # Include role in the serializer  
        ]

    def get_profile_photo_url(self, obj):
        return obj.profile_photo_public_url

    def update(self, instance, validated_data):
        user_data = validated_data.pop('user', {})
        user = instance.user

        if 'username' in user_data:
            user.username = user_data['username']
        if 'first_name' in user_data:
            user.first_name = user_data['first_name']
        if 'last_name' in user_data:
            user.last_name = user_data['last_name']
        if 'password' in validated_data:
            user.set_password(validated_data['password'])

        user.save()
        return super().update(instance, validated_data)


from rest_framework import serializers
from .models import ChatThread, Message
from django.contrib.auth import get_user_model

User = get_user_model()

class UserMiniSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username']

class ChatThreadSerializer(serializers.ModelSerializer):
    user = UserMiniSerializer()
    analyst = UserMiniSerializer()

    class Meta:
        model = ChatThread
        fields = "__all__"

class MessageSerializer(serializers.ModelSerializer):
    sender = UserMiniSerializer()

    class Meta:
        model = Ana_Message
        fields = "__all__"




# =====================================================================================================================================
from rest_framework import serializers
from .models import PlatformWalkthroughVideo

class PlatformWalkthroughVideoSerializer(serializers.ModelSerializer):
    video_url = serializers.ReadOnlyField()
    thumbnail_url = serializers.ReadOnlyField()

    class Meta:
        model = PlatformWalkthroughVideo
        fields = [
            "id",
            "title",
            "description",
            "author_name",
            "author_role",
            "author_image",
            "schedule_days",
            "schedule_time",
            "is_verified",
            "uploaded_at",
            "video_url",
            "thumbnail_url",
        ]




# ********************************************************************************************************************************************************************************

# from .models import Webinar
# class WebinarSerializer(serializers.ModelSerializer):
#     registered_count = serializers.SerializerMethodField()

#     class Meta:
#         model = Webinar
#         fields = '__all__'

#     def get_registered_count(self, obj):
#         return obj.registered_users.count()

from rest_framework import serializers
from .models import Webinar

class WebinarSerializer(serializers.ModelSerializer):
    registered_count = serializers.SerializerMethodField()
    already_registered = serializers.SerializerMethodField() 
    thumbnail_public_url = serializers.SerializerMethodField()

    class Meta:
        model = Webinar
        fields = '__all__' 
        
    def get_registered_count(self, obj):
        return obj.registered_users.count()

    def get_already_registered(self, obj):
        request = self.context.get('request')
        if request and hasattr(request, 'user'):
            return obj.registered_users.filter(id=request.user.id).exists()
        return False
    
    def get_thumbnail_public_url(self, obj):
        return obj.thumbnail_public_url

# ********************************************************************************************************************************************************************************

from rest_framework import serializers
from .models import CallCredit, Session

class CallCreditSerializer(serializers.ModelSerializer):
    class Meta:
        model = CallCredit
        fields = ['id', 'user', 'hours_remaining']

class SessionSerializer(serializers.ModelSerializer):
    user_name = serializers.CharField(source='user.username', read_only=True)
    analyst_name = serializers.CharField(source='analyst.username', read_only=True)

    class Meta:
        model = Session
        fields = '__all__'
        extra_kwargs = {
            'user': {'read_only': True}
        }

# ********************************************************************************************************************************************************************************

from rest_framework import serializers
from .models import FeatureRequest, Vote

class FeatureRequestSerializer(serializers.ModelSerializer):
    votes_count = serializers.SerializerMethodField()

    class Meta:
        model = FeatureRequest
        fields = "__all__"
        read_only_fields = ['created_by'] 

    def get_votes_count(self, obj):
        return obj.votes.count()

class VoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vote
        fields = "__all__"

# ********************************************************************************************************************************************************************************



from rest_framework import serializers
from .models import Challenge, ChallengeParticipant
from rest_framework import serializers
from .models import Challenge, ChallengeParticipant
# class ChallengeSerializer(serializers.ModelSerializer):
#     is_joined = serializers.SerializerMethodField()
#     participant_id = serializers.SerializerMethodField()
#     participants_count = serializers.SerializerMethodField()  # ✅ added dynamic field

#     class Meta:
#         model = Challenge
#         fields = '__all__'  # Includes is_joined, participant_id, participants_count

#     def get_is_joined(self, obj):
#         request = self.context.get("request")
#         user = request.user if request else None
#         if not user or user.is_anonymous:
#             return False
#         return ChallengeParticipant.objects.filter(user=user, challenge=obj).exists()

#     def get_participant_id(self, obj):
#         request = self.context.get("request")
#         user = request.user if request else None
#         if not user or user.is_anonymous:
#             return None
#         try:
#             participant = ChallengeParticipant.objects.get(user=user, challenge=obj)
#             return participant.id
#         except ChallengeParticipant.DoesNotExist:
#             return None

#     def get_participants_count(self, obj):
#         return obj.participants.count()  # ✅ use reverse relation for live count

class ChallengeSerializer(serializers.ModelSerializer):
    is_joined = serializers.SerializerMethodField()
    participant_id = serializers.SerializerMethodField()
    participants_count = serializers.SerializerMethodField()
    nft_rewards = serializers.SerializerMethodField()
    user_position = serializers.SerializerMethodField()  # ✅ NEW

    class Meta:
        model = Challenge
        fields = '__all__'  # includes all above

    def get_is_joined(self, obj):
        user = self.context['request'].user
        return ChallengeParticipant.objects.filter(user=user, challenge=obj).exists()

    def get_participant_id(self, obj):
        user = self.context['request'].user
        try:
            return ChallengeParticipant.objects.get(user=user, challenge=obj).id
        except ChallengeParticipant.DoesNotExist:
            return None

    def get_participants_count(self, obj):
        return obj.participants.count()

    def get_user_position(self, obj):
        user = self.context['request'].user
        try:
            part = ChallengeParticipant.objects.get(user=user, challenge=obj)
            return part.leaderboard_position
        except ChallengeParticipant.DoesNotExist:
            return None

    def get_nft_rewards(self, obj):
        user = self.context['request'].user
        badges = NFTBadge.objects.filter(linked_challenge=obj)
        result = []

        category_position_map = {
            'first': 1,
            'second': 2,
            'third': 3,
            'fourth': 4,
            'fifth': 5,
            'six': 6,
            'seven': 7,
            'eight': 8,
            'nin': 9,
            'ten': 10,
        }

        for badge in badges:
            category = badge.category
            required_position = category_position_map.get(category, None)

            result.append({
                "id": badge.id,
                "name": badge.name,
                "category": category,
                "description": badge.description,
                "image_url": badge.image_public_url,
                "position_required": required_position,
                "unlocked": badge.linked_user == user
            })

        return result

from .serializers import UserProfileSerializer  
from .models import *
class ChallengeParticipantSerializer(serializers.ModelSerializer):
    screenshot_url = serializers.SerializerMethodField()
    challenge = serializers.IntegerField(write_only=True)
    user_profile = serializers.SerializerMethodField()
    leaderboard_position = serializers.IntegerField(read_only=True)
    unlocked_badge = serializers.SerializerMethodField()  # ✅ NEW

    class Meta:
        model = ChallengeParticipant
        fields = [
            'id', 'user', 'challenge', 'answers', 'screenshots',
            'screenshot_url', 'leaderboard_position', 'created_at', 'user_profile',
             'unlocked_badge'
        ]
        read_only_fields = ['user']

    def get_screenshot_url(self, obj):
        return obj.screenshot_public_url

    def get_user_profile(self, obj):
        try:
            from .models import UserProfiles 
            profile = UserProfiles.objects.get(user=obj.user)
            return UserProfileSerializer(profile).data
        except UserProfiles.DoesNotExist:
            return None
    def get_unlocked_badge(self, obj):
        badge = NFTBadge.objects.filter(linked_user=obj.user, linked_challenge=obj.challenge).first()
        if badge:
            return {
                "id": badge.id,
                "name": badge.name,
                "category": badge.category,
                "image_url": badge.image_public_url
            }
        return None


# class NFTBadgeSerializer(serializers.ModelSerializer):
#     image_url = serializers.SerializerMethodField()

#     class Meta:
#         model = NFTBadge
#         fields = ['id', 'name', 'category', 'image_url', 'description', 'manually_assignable',
#                   'linked_user', 'linked_challenge', 'assigned_at']

#     def get_image_url(self, obj):
#         return obj.image_public_url


# ===============================================================================-








class VideoSerializer(serializers.ModelSerializer):
    # ---------- read‑only helpers ----------
    public_url     = serializers.SerializerMethodField()

    class Meta:
        model  = Video
        fields = [
            "id",
            "title",
            "video_file",          # upload or existing file
            "manual_video_url",
            "thumbnail_url",        # plain string field
            "public_url",
            "uploaded_at",
            "course_level",
        ]
        extra_kwargs = {
            "thumbnail": {"write_only": True, "required": False},
            "video_file": {"required": False},
        }

    # ---------- helper getters ------------
    def get_public_url(self, obj):
        return obj.public_url


class CourseLevelSerializer(serializers.ModelSerializer):
    videos = VideoSerializer(many=True, read_only=True)

    class Meta:
        model = CourseLevel
        fields = '__all__'


class CourseSerializer(serializers.ModelSerializer):
    levels = CourseLevelSerializer(many=True, read_only=True)

    class Meta:
        model = Course
        fields = '__all__'



class NoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Note
        fields = '__all__'



class MCQQuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = MCQQuestion
        fields = '__all__'
        
        
class CourseEnrollmentSerializer(serializers.ModelSerializer):
    course_title = serializers.CharField(source='course.title', read_only=True)

    class Meta:
        model = CourseEnrollment
        fields = ['id', 'course', 'course_title', 'enrolled_at']

# ********************************************************************************************************************************************************************************







# Serailizer for the platnium member journel notes:
class TradeJournalEntrySerializer(serializers.ModelSerializer):
    class Meta:
        model = TradeJournalEntry
        fields = '__all__'
        read_only_fields = ['user', 'created_at']

#  View to create and list entries for the logged-in user
class TradeJournalListCreateView(generics.ListCreateAPIView):
    serializer_class = TradeJournalEntrySerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return TradeJournalEntry.objects.filter(user=self.request.user).order_by('-created_at')

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


# ********************************************************************************************************************************************************************************
# For Chating

from rest_framework import serializers
from .models import Message, Conversation

from rest_framework import serializers
from .models import Message, Conversation
from django.contrib.auth import get_user_model

User = get_user_model()

from rest_framework import serializers
from .models import Message, Conversation

class MessageSerializer(serializers.ModelSerializer):
    sender_name = serializers.CharField(source='sender.username', read_only=True)
    sender_profile_photo_url = serializers.SerializerMethodField()

    class Meta:
        model = Message
        fields = ['id', 'conversation', 'sender', 'sender_name', 'sender_profile_photo_url', 'content', 'timestamp', 'is_read', 'is_notification']
        
        extra_kwargs = {
            'sender': {'read_only': True}
        }

    def get_sender_profile_photo_url(self, obj):
        try:
            return obj.sender.profile.profile_photo_public_url
        except Exception:
            return None

class ConversationSerializer(serializers.ModelSerializer):
    messages = MessageSerializer(many=True, read_only=True)
    participants = serializers.StringRelatedField(many=True)

    class Meta:
        model = Conversation
        fields = ['id', 'participants', 'messages']

# one to one chat 
from rest_framework import serializers
from .models import AnalystChat, AnalystMessage
from django.contrib.auth import get_user_model

User = get_user_model()

class AnalystMessageSerializer(serializers.ModelSerializer):
    sender_name = serializers.CharField(source='sender.username', read_only=True)

    class Meta:
        model = AnalystMessage
        fields = ['id', 'chat', 'sender', 'sender_name', 'content', 'timestamp', 'is_read']
        extra_kwargs = {
            'sender': {'read_only': True}
        }

class AnalystChatSerializer(serializers.ModelSerializer):
    messages = AnalystMessageSerializer(many=True, read_only=True)
    analyst_username = serializers.CharField(source='analyst.username', read_only=True)

    class Meta:
        model = AnalystChat
        fields = ['id', 'user', 'analyst', 'analyst_username', 'messages']





# ********************************************************************************************************************************************************************************
# For Notifications
from rest_framework import serializers
from .models import Notification

class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = ['id', 'title', 'message', 'is_read', 'created_at']




# =========================================================================================================
from rest_framework import serializers
from .models import (
    BeginnerHubCourse,
    BeginnerHubVideo,

)

class BeginnerHubCourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = BeginnerHubCourse
        fields = ['id', 'title', 'description', 'category']
        
class BeginnerHubVideoSerializer(serializers.ModelSerializer):
    video_url = serializers.ReadOnlyField()
    thumbnail_url = serializers.ReadOnlyField()

    class Meta:
        model = BeginnerHubVideo
        fields = ['id', 'title', 'description', 'video_url', 'thumbnail_url']






# =========================================================================================================
# for contact us form of the wealthseries
from rest_framework import serializers

class SalesInquirySerializer(serializers.Serializer):
    name = serializers.CharField(max_length=255)
    email = serializers.EmailField()
    phone = serializers.CharField(max_length=20)
    subject = serializers.CharField(max_length=255)
    message = serializers.CharField()
    inquiry_type = serializers.CharField(required=False)


# =========================================================================================================
# for contact us form of the trainingcontact us form for mentorship
from rest_framework import serializers

class TrainingContactSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=255)
    email = serializers.EmailField()
    phone = serializers.CharField(max_length=20)
    inquiry_type = serializers.CharField(max_length=100)



from rest_framework import serializers
from .models import WeeklyBriefing, TradeIdea

class TradeIdeaSerializer(serializers.ModelSerializer):
    class Meta:
        model = TradeIdea
        fields = ['ticker', 'target_price', 'stop_loss', 'timeframe', 'direction']

class WeeklyBriefingSerializer(serializers.ModelSerializer):
    trade_ideas = TradeIdeaSerializer(many=True, read_only=True)
    public_url = serializers.SerializerMethodField()
    thumbnail_public_url = serializers.SerializerMethodField()

    class Meta:
        model = WeeklyBriefing
        fields = [
            'id', 'title', 'video_url', 'manual_video_url', 'published_date',
            'duration', 'analyst_name', 'analyst_title', 'summary',
            'key_points', 'thumbnail', 'thumbnail_public_url', 'trade_ideas', 'public_url'
        ]

    def get_public_url(self, obj):
        return obj.manual_video_url or obj.video_url

    def get_thumbnail_public_url(self, obj):
        if obj.thumbnail:
            return f"https://pub-552c13ad8f084b0ca3d7b5aa8ddb03a7.r2.dev/{obj.thumbnail.name}"
        return None


# ==========================================================================================================================

from rest_framework import serializers
from .models import SectorExposure

class SectorExposureSerializer(serializers.ModelSerializer):
    class Meta:
        model = SectorExposure
        fields = ['data']
        
        
        




# =========================================================
# Landing page blogs
from rest_framework import serializers
from .models import EditorsChoice

class EditorsChoiceSerializer(serializers.ModelSerializer):
    image_url = serializers.ReadOnlyField()

    class Meta:
        model = EditorsChoice
        fields = ['id', 'title', 'category', 'description', 'slug', 'image_url']
