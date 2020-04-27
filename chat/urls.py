from django.urls import path, re_path


from .views import home, sendMessage, InboxView, ThreadView


urlpatterns = [
    path("", InboxView.as_view()),
    re_path(r"^(?P<username>[\w.@+-]+)", home),
    path("<username>/", home, name="message"),
    path("sendMessage/", sendMessage, name="sendMessage"),
]
