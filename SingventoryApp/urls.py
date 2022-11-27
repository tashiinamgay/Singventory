from django.urls import path

from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.home, name='login'),
    path('reg/', views.reg, name="reg"),

    # User
    path('about/', views.userabout, name="userabout"),
    path(r'equipment/?P<pk>[0-9]+/$', views.useritem, name="useritem"),
    path('home/', views.userhome, name="userhome"),
    path('equipment/', views.userequip, name="userequip"),
    path('home/<pk>', views.categoryview, name='categoryview'),

    path('profile/', views.userprofile, name="userprofile"),
    path('profile/edit/', views.userprofileupdate, name="userprofileedit"),

    path('return/<pk>', views.userReturn, name='return'),
    path('return/borrowed/<pk>', views.userReturnPage, name='returnPage'),
    path('cancel/<pk>', views.userCancel, name='cancel'),
    path('unread/<pk>', views.notifRead, name='unread'),

    path('search/', views.searchBar, name='search'),



    # Admin
    path('svadmin/', views.adminHome, name='adminhome'),
    path('svadmin/profile', views.adminProfile, name='adminprofile'),
    path('svadmin/profile/edit', views.adminProfileUpdate, name='adminprofileupdate'),
    path('svadmin/view/user', views.adminViewUser, name='viewuser'),
    path('svadmin/view/equipment', views.adminViewEquipment, name='viewequipment'),
    path('svadmin/view/category', views.adminViewCategory, name='viewcat'),

    path('svadmin/add/category', views.adminAddCategory, name='addcat'),
    path('svadmin/add/equipment', views.adminAddEquipment, name='addequip'),
    path('svadmin/add/user', views.adminAddUser, name='adduser'),

    path(r'svadmin/edit/user/?P<pk>[0-9]+/$', views.adminEditUser, name='editUser'),
    path('svadmin/edit/category/<pk>', views.adminEditCategory, name='editCat'),
    path('svadmin/edit/equipment/<pk>', views.adminEditEquipment, name='editEquip'),

    path('svadmin/del/user/<pk>', views.adminDelUser, name='delUser'),
    path('svadmin/del/category/<pk>', views.adminDelCategory, name='delCat'),
    path('svadmin/del/equipment/<pk>', views.adminDelEquipment, name='delEquip'),

    path('svadmin/approve/<pk>', views.adminApprove, name='approve'),
    path('svadmin/approveConfirm/<pk>', views.approveConfirm, name='approveConfirm'),
    path('svadmin/reject/<pk>', views.adminReject, name='reject'),
    path('svadmin/return/<pk>', views.adminReturnConfirm, name='adminReturn'),


    path('logout/', views.logout_view, name='logout'),
   
    #forgot password urls
    path('reset_password/', auth_views.PasswordResetView.as_view(template_name="SingventoryApp/reset_password.html"), name="reset_password"),
    
    path('reset_password_sent/', auth_views.PasswordResetDoneView.as_view(template_name="SingventoryApp/reset_password_sent.html"), name="password_reset_done"),

    path('reset/<uidb64>/<token>', auth_views.PasswordResetConfirmView.as_view(template_name="SingventoryApp/reset.html"), name="password_reset_confirm"),

    path('reset_password_complete/', auth_views.PasswordResetCompleteView.as_view(template_name="SingventoryApp/reset_password_complete.html"), name="password_reset_complete"),

    path('activate_user/<uidb64>/<token>', views.activate, name='activate'),

]