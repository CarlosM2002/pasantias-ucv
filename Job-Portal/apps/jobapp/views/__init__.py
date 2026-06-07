from .employee import ApplyJobView, DeleteApplicantView, DeleteBookmarkView, JobBookmarkView
from .employer import (
    AllApplicantsView,
    ApplicantDetailsView,
    CreateJobView,
    DeleteJobView,
    JobEditView,
    MakeCompleteJobView,
    UpdateApplicantStatusView,
)
from .public import JobListView, SearchResultView, SingleJobView, home_view, about_view
from .shared import admin_report_view, dashboard_view, toggle_employer_privileges

