from django.urls import path
from jobapp.views import (
    AllApplicantsView,
    ApplicantDetailsView,
    ApplyJobView,
    CreateJobView,
    about_view,
    admin_report_view,
    dashboard_view,
    DeleteBookmarkView,
    DeleteJobView,
    home_view,
    JobBookmarkView,
    JobEditView,
    JobListView,
    MakeCompleteJobView,
    SearchResultView,
    SingleJobView,
    UpdateApplicantStatusView,
    toggle_employer_privileges,
)

app_name = "jobapp"

urlpatterns = [
    path('', home_view, name='home'),
    path('jobs/', JobListView.as_view(), name='job-list'),
    path('job/create/', CreateJobView.as_view(), name='create-job'),
    path('job/<int:id>/', SingleJobView.as_view(), name='single-job'),
    path('apply-job/<int:id>/', ApplyJobView.as_view(), name='apply-job'),
    path('bookmark-job/<int:id>/', JobBookmarkView.as_view(), name='bookmark-job'),
    path('about/', about_view, name='about'),
    path('result/', SearchResultView.as_view(), name='search_result'),
    path('dashboard/', dashboard_view, name='dashboard'),
    path('dashboard/admin/report/', admin_report_view, name='admin-report'),
    path('dashboard/admin/employer/<int:user_id>/privileges/<str:action>/', toggle_employer_privileges, name='set-employer-privileges'),
    path('dashboard/employer/job/<int:id>/applicants/', AllApplicantsView.as_view(), name='applicants'),
    path('dashboard/employer/job/edit/<int:id>', JobEditView.as_view(), name='edit-job'),
    path('dashboard/employer/applicant/<int:id>/', ApplicantDetailsView.as_view(), name='applicant-details'),
    path('dashboard/employer/close/<int:id>/', MakeCompleteJobView.as_view(), name='complete'),
    path('dashboard/employer/delete/<int:id>/', DeleteJobView.as_view(), name='delete'),
    path('dashboard/employer/applicant/update-status/<int:id>/', UpdateApplicantStatusView.as_view(), name='update-applicant-status'),
    path('dashboard/employee/delete-bookmark/<int:id>/', DeleteBookmarkView.as_view(), name='delete-bookmark'),
]
