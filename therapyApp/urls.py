from django.urls import path
from . import views

urlpatterns = [
    path("", views.signin, name="signin"),
    path("signup/", views.signup, name="signup"),
    path("signout/", views.signout, name="signout"),
    path("index/", views.index, name="index"),
    path("dash/", views.dash, name="dash"),
    path("payments/", views.payments, name="payments"),
    path("therapist/", views.therapist, name="therapist"),
    path("session/", views.session, name="session"),
    path("therapist-desc/<int:id>", views.therapist_desc, name="therapist-desc"),
    path("client/", views.client, name="client"),
    path("update/<int:id>", views.update, name="update")
]