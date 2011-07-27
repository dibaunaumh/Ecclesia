OPENID_REDIRECT_NEXT = '/accounts/openid/done/'

OPENID_SREG = {"requred": "nickname, email, fullname",
               "optional":"postcode, country",
               "policy_url": ""}

#example should be something more like the real thing, i think
OPENID_AX = [{"type_uri": "http://axschema.org/contact/email",
              "count": 1,
              "required": True,
              "alias": "email"},
             {"type_uri": "http://axschema.org/schema/fullname",
              "count":1 ,
              "required": False,
              "alias": "fname"}]

OPENID_AX_PROVIDER_MAP = {'Google': {'email': 'http://axschema.org/contact/email',
                                     'firstname': 'http://axschema.org/namePerson/first',
                                     'lastname': 'http://axschema.org/namePerson/last'},
                          'Default': {'email': 'http://axschema.org/contact/email',
                                      'fullname': 'http://axschema.org/namePerson',
                                      'nickname': 'http://axschema.org/namePerson/friendly'}
                          }

TWITTER_CONSUMER_KEY = 'tNEzCcq6vy5zLaJmfpLAA'
TWITTER_CONSUMER_SECRET = 'BwR4YrOtR0YMdt10r5rGraKvk25ZGEuiogbOx6cg5Bw'

FACEBOOK_APP_ID = '115782818510137'
FACEBOOK_API_KEY = '0524e8ea9d6e5a193a74c83a8e18b111'
FACEBOOK_SECRET_KEY = '58a1bf1057cd12606e161d4130586502'

LINKEDIN_CONSUMER_KEY = '11iEwCbjusHiIDBkcOSyhJ3yMvF2yko8BnXVZtxAfz6cvn1PJYk_Qg9yVrwbHSfR'
LINKEDIN_CONSUMER_SECRET = 'CqCW86cXwr3Upyenw5VjzhHsiNnKj2qeSLh3BxPNuIcT8FGy0PVMNfcCmzzjXWCK'

## if any of this information is desired for your app
FACEBOOK_EXTENDED_PERMISSIONS = (
    'publish_stream',
    #'create_event',
    #'rsvp_event',
    #'sms',
    #'offline_access',
    #'email',
    'read_stream',
    #'user_about_me',
    #'user_activites',
    #'user_birthday',
    #'user_education_history',
    #'user_events',
    #'user_groups',
    #'user_hometown',
    #'user_interests',
    #'user_likes',
    #'user_location',
    #'user_notes',
    #'user_online_presence',
    #'user_photo_video_tags',
    #'user_photos',
    #'user_relationships',
    #'user_religion_politics',
    #'user_status',
    #'user_videos',
    #'user_website',
    #'user_work_history',
    #'read_friendlists',
    #'read_requests',
    #'friend_about_me',
    #'friend_activites',
    #'friend_birthday',
    #'friend_education_history',
    #'friend_events',
    #'friend_groups',
    #'friend_hometown',
    #'friend_interests',
    #'friend_likes',
    #'friend_location',
    #'friend_notes',
    #'friend_online_presence',
    #'friend_photo_video_tags',
    #'friend_photos',
    #'friend_relationships',
    #'friend_religion_politics',
    #'friend_status',
    #'friend_videos',
    #'friend_website',
    #'friend_work_history',
)


AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
    'socialauth.auth_backends.OpenIdBackend',
    'socialauth.auth_backends.TwitterBackend',
    'socialauth.auth_backends.FacebookBackend',
    'socialauth.auth_backends.LinkedInBackend',
)
