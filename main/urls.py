from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include
from .views import (
#     CourseListAPIView,
#     EnrollCourseAPIView,
#     CourseLevelsAPIView,
#     LevelVideosAPIView,
#     VideoDetailAPIView,
#     CompleteVideoAPIView,
#     QuizDetailAPIView,
#     SubmitQuizAPIView,
#     LevelExamDetailAPIView,
#     SubmitExamAPIView,
#     CourseDetailAPIView,
#     LevelProgressAPIView,
#    CourseVideosAPIView, 

    # # stock_market_search_view,
    # stock_market_news_view,
    # technology_news_view,
    # stock_news_view,
    # recent_news_view,
    # crypto_news_view,
    # stock_data_view,
    # For contact us 
    request_demo,
    contact_us,
    # for dark pool
    xlsx_data_view_large_caps,
    xlsx_data_view_medium_caps,
    xlsx_data_view_small_caps,
    xlsx_data_view_large_caps_down,
    xlsx_data_view_medium_caps_down,
    xlsx_data_view_small_caps_down,
    alerts_xlsx_data_view_large_caps,
    alerts_xlsx_data_view_large_caps_down,
    alerts_xlsx_data_view_medium_caps,
    alerts_xlsx_data_view_medium_caps_down,
    alerts_xlsx_data_view_small_caps,
    alerts_xlsx_data_view_small_caps_down,
    TradeJournalListCreateView,
     CallCreditViewSet, SessionViewSet,
     
    



)
from .views import UserProfileDetailView

from rest_framework.routers import DefaultRouter
from main.views import  *
# (CourseViewSet, CourseLevelViewSet, VideoViewSet, mark_video_watched, get_course_progress, NoteViewSet, NotesByLevelAPIView,
#                          MCQQuestionListAPIView, SubmitQuizAPIView,UserProfileDetailView, all_courses_progress,
#                          WebinarListCreateView, WebinarRetrieveUpdateDestroyView, register_for_webinar, unregister_from_webinar,
#                             MyConversationsView, SendMessageView, TradeJournalListCreateView,
#                             user_list, FeatureRequestViewSet,

#                             ChallengeViewSet, ChallengeParticipantViewSet,

#                             # ChallengeListView,
#                             # JoinChallengeView,
#                             # UpdatePerformanceView,
#                             # ChallengeLeaderboardView,
#                             # MyChallengePerformanceView,
#                             # OverallLeaderboardView,
#                             NotificationListView,
#                             MarkNotificationAsReadView,
#                             unread_counts,
#                             challenge_leaderboard,
#                             # BeginnerHubCourseListView,
#                             # BeginnerHubSectionListView,
#                             # BeginnerHubVideoListView,
#                             # save_beginnerhub_progress,
#                             # get_beginnerhub_progress,
#                             TradeGPTTokenView,
#                             SalesContactView,
#                             TrainingContactView,
#                             weekly_large_caps_up_view, weekly_large_caps_down_view,
#     weekly_medium_caps_up_view, weekly_medium_caps_down_view,
#     weekly_small_caps_up_view, weekly_small_caps_down_view,
#       intraday_large_caps_up_view,
#     intraday_large_caps_down_view,
#     intraday_medium_caps_up_view,
#     intraday_medium_caps_down_view,
#     intraday_small_caps_up_view,
#     intraday_small_caps_down_view,
  
#     MarketNewsAPIView,
#     PlatinumBriefingListAPIView,
#     CoursesByCategory, CourseVideosView, VideoDetailView,
#     create_mux_stream,
#     MT5SnapshotUploadView,
#     PortfolioSummaryView,
#     SectorExposureView,
#     AISuggestionsView,
#     start_analyst_chat,
#     AnalystChatDetailView,
#     AnalystMessageCreateView,
#     assigned_analyst,
#     subscribe_newsletter,
#     footer_subscribe,
#     leave_review,
#     request_call_credits,
#     SectorIQView,
#     DiversificationScoreView,
#     EditorsChoiceListView,
#     ensure_analyst_chat,
    

                            

# )



from .views import WebinarViewSet
from rest_framework.routers import DefaultRouter
routerweb = DefaultRouter()
routerweb.register(r'webinars', WebinarViewSet, basename='webinar')


router = DefaultRouter()
router.register('courses', CourseViewSet)
router.register('levels', CourseLevelViewSet)
router.register('videos', VideoViewSet)
router.register(r'notes', NoteViewSet)

# This is for the session call/ call credit paltinum dashboard
routersch = DefaultRouter()
routersch.register(r'callcredits', CallCreditViewSet, basename='callcredits')
routersch.register(r'sessions', SessionViewSet, basename='sessions')


# Feature Voting
featurerouter = DefaultRouter()
featurerouter.register(r'features', FeatureRequestViewSet, basename='features')

challengerouter = DefaultRouter()
challengerouter.register(r'challenges', ChallengeViewSet, basename='challenges')
challengerouter.register(r'challenge-participants', ChallengeParticipantViewSet, basename='challenge-participants')




urlpatterns = [
  

    # user endpoints
    path('api/user/profile/', UserProfileDetailView.as_view(), name='user-profile-detail'),
    # impersonate user login
    path('api/admin/impersonate/', ImpersonateUserView.as_view(), name='impersonate-user'),

    path("api/generate-tradegpt-token/", TradeGPTTokenView.as_view(), name="generate-tradegpt-token"),
    
    # for platinum member user list all user:
    path('api/users/', user_list, name='user-list'),



    path('', include(router.urls)),
    path('videos/<int:video_id>/watch/', mark_video_watched, name='mark-video-watched'),
    path('courses/<int:course_id>/progress/', get_course_progress, name='get-course-progress'),
    path('courses/<int:course_id>/levels/<int:level_id>/notes/', NotesByLevelAPIView.as_view()),
    
    path('courses/<int:course_id>/levels/<int:level_id>/mcqs/', MCQQuestionListAPIView.as_view()),
    path('courses/<int:course_id>/levels/<int:level_id>/mcqs/submit/', SubmitQuizAPIView.as_view()),
    path('user/courses/progress/', all_courses_progress, name='all-courses-progress'),


    # platfomr walkthrough
    path('api/platform-walkthrough/', PlatformWalkthroughVideoListView.as_view(), name='platform-walkthrough-list'),

    # For Platinum Member:
    path('api/trade-journal/', TradeJournalListCreateView.as_view(), name='trade-journal'),
    #  path('api/', include(routerweb.urls)),
    path('api/webinars/', WebinarListCreateView.as_view(), name='webinar-list-create'),
    path('api/webinars/<int:pk>/', WebinarRetrieveUpdateDestroyView.as_view(), name='webinar-detail'),
    path('api/webinars/<int:pk>/register/', register_for_webinar, name='webinar-register'),
    path('api/webinars/<int:pk>/unregister/', unregister_from_webinar, name='webinar-unregister'),

    
    # For chat:
    path('api/chat/my-conversations/', MyConversationsView.as_view()),
    path('api/chat/send/', SendMessageView.as_view()),
    
    
    path("api/analyst-chat/start/", start_analyst_chat),
    path("api/analyst-chat/", AnalystChatDetailView.as_view()),
    path("api/analyst-chat/send/", AnalystMessageCreateView.as_view()),
    path("api/assigned-analyst/", assigned_analyst, name="assigned_analyst"),
    path("api/analyst-chat/ensure/", ensure_analyst_chat),
    path('api/analyst-messages/', AnalystMessageListView.as_view(), name='analyst-messages'),


    # for session call
    path('api/', include(routersch.urls)),
    path('api/', include(featurerouter.urls)),
    path('api/request-call-credits/', request_call_credits, name='request_call_credits'),

    # Challenge Routes
    path('api/', include(challengerouter.urls)),
    path('api/challenges/<int:pk>/leaderboard/', challenge_leaderboard),

    #For notification platinum member
    path('api/notifications/', NotificationListView.as_view(), name='notifications'),
    path('api/notifications/<int:pk>/read/', MarkNotificationAsReadView.as_view(), name='mark-notification-read'),
    path("api/chat/unread-count/", unread_counts),
    
    
    # for live streaming
    path("api/mux/create-stream/", create_mux_stream),



    # For platinum member weekly briefing
    path("api/weekly-briefings/", PlatinumBriefingListAPIView.as_view(), name="weekly-briefings"),


    # For News 
    path("api/market-news/", MarketNewsAPIView.as_view(), name="market-news"), 

    # for Beginer hub
    path('api/beginnerhub/courses/<str:category>/', CoursesByCategory.as_view(), name='courses-by-category'),
    path('api/beginnerhub/courses/<int:course_id>/videos/', CourseVideosView.as_view(), name='course-videos'),
    path('api/beginnerhub/videos/<int:id>/', VideoDetailView.as_view(), name='video-detail'),


  # landing page blog
   path('api/editors-choice/', EditorsChoiceListView.as_view(), name='editors-choice'),
   path('editors-choice/<slug:slug>/', EditorsChoiceDetailView.as_view()), 
   
    # for smtp -contact us
    path('api/request-demo/', request_demo, name='request_demo'),
    path('api/contact-us/', contact_us, name='contact-us'),
    path('api/newsletter/subscribe/', subscribe_newsletter, name='subscribe_newsletter'),
    path('api/footer-subscribe/', footer_subscribe, name='footer_subscribe'),
    path('api/leave-review/', leave_review, name='leave_review'),
     
    # for contact us form of the wealthseries
    path("api/sales-inquiry/", SalesContactView.as_view(), name="sales-inquiry"),
    # for mentorship card training contact us form 
    path("api/training-inquiry/", TrainingContactView.as_view(), name="training-inquiry"),


    # Platinum member portfolio heatmap
    path('api/mt5-snapshot/', MT5SnapshotUploadView.as_view()),
    path("api/portfolio/", PortfolioSummaryView.as_view(), name="portfolio-summary"),
    path("api/portfolio/sector-exposure/", SectorExposureView.as_view(), name="sector-exposure"),
    path("api/portfolio/ai-suggestions/", AISuggestionsView.as_view(), name="ai-suggestions"),
    path("api/portfolio/sector-iq/", SectorIQView.as_view()),
    path("api/portfolio/diversification/", DiversificationScoreView.as_view()),
    



    # UpTrend api
    path('api/Large_caps/', xlsx_data_view_large_caps, name='xlsx_data_view_large_caps'),
    path('api/Medium_caps/', xlsx_data_view_medium_caps, name='xlsx_data_view_medium_caps'),
    path('api/Small_caps/', xlsx_data_view_small_caps, name='xlsx_data_view_small_caps'),

    # Downtrend APIs
    path('api/large_caps_down/', xlsx_data_view_large_caps_down, name='xlsx_data_view_large_caps_down'),
    path('api/medium_caps_down/', xlsx_data_view_medium_caps_down, name='xlsx_data_view_medium_caps_down'),
    path('api/small_caps_down/', xlsx_data_view_small_caps_down, name='xlsx_data_view_small_caps_down'),


    # for trade alerts
     # UpTrend APIs
    path('api/alerts/large_caps/', alerts_xlsx_data_view_large_caps, name='alerts_xlsx_data_view_large_caps'),
    path('api/alerts/medium_caps/', alerts_xlsx_data_view_medium_caps, name='alerts_xlsx_data_view_medium_caps'),
    path('api/alerts/small_caps/', alerts_xlsx_data_view_small_caps, name='alerts_xlsx_data_view_small_caps'),

    # DownTrend APIs
    path('api/alerts/large_caps_down/', alerts_xlsx_data_view_large_caps_down, name='alerts_xlsx_data_view_large_caps_down'),
    path('api/alerts/medium_caps_down/', alerts_xlsx_data_view_medium_caps_down, name='alerts_xlsx_data_view_medium_caps_down'),
    path('api/alerts/small_caps_down/', alerts_xlsx_data_view_small_caps_down, name='alerts_xlsx_data_view_small_caps_down'),


    
    # Intraday Up APIs
    path('api/intraday/large_caps/', intraday_large_caps_up_view, name='intraday_large_caps_up'),
    path('api/intraday/medium_caps/', intraday_medium_caps_up_view, name='intraday_medium_caps_up'),
    path('api/intraday/small_caps/', intraday_small_caps_up_view, name='intraday_small_caps_up'),
    

    # Intraday Down APIs
    path('api/intraday/large_caps_down/', intraday_large_caps_down_view, name='intraday_large_caps_down'),
    path('api/intraday/medium_caps_down/', intraday_medium_caps_down_view, name='intraday_medium_caps_down'),
    path('api/intraday/small_caps_down/', intraday_small_caps_down_view, name='intraday_small_caps_down'),

  # Weekly Up APIs
    path('api/weekly/large_caps/', weekly_large_caps_up_view, name='weekly_large_caps_up'),
    path('api/weekly/medium_caps/', weekly_medium_caps_up_view, name='weekly_medium_caps_up'),
    path('api/weekly/small_caps/', weekly_small_caps_up_view, name='weekly_small_caps_up'),

    # Weekly Down APIs
    path('api/weekly/large_caps_down/', weekly_large_caps_down_view, name='weekly_large_caps_down'),
    path('api/weekly/medium_caps_down/', weekly_medium_caps_down_view, name='weekly_medium_caps_down'),
    path('api/weekly/small_caps_down/', weekly_small_caps_down_view, name='weekly_small_caps_down'),


  # Ticker api
    # path("api/tickers/", tickers_data_view),
    # path('api/tickers/data/', ticker_data_api, name='tickers-data'),

]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
