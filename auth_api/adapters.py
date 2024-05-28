from allauth.socialaccount.providers.google.views import GoogleOAuth2Adapter


class CustomGoogleOAuth2Adapter(GoogleOAuth2Adapter):
    def get_scope(self, request=None):
        return super().get_scope()
