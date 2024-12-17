
from django.urls import path, include, re_path
from invitations.views import referralRedirect, referralSignup, handleExcelFile,fileuploadMenu, emailpreview,share

urlpatterns =[
    path("accounts/",include("django.contrib.auth.urls")),
    re_path("accounts/ref/(?P<refkey>[^/.]+)/$",referralRedirect, name="referral"),
    re_path("accounts/signup",referralSignup, name="referralSignup"),
    #path("accounts/signup",signup,name = "signup"),
    #path("accounts/bulkadd/",bulkAdd,name="bulkadd"),
    path("upload/invexcel/", handleExcelFile, name = "uploadexcel"),
    path("fileupload/", fileuploadMenu, name = "fileupload"),
    path("admin/invitations/emailpreview/<int:pk>/", emailpreview),
    path("api/share/",share,name="share")
]
