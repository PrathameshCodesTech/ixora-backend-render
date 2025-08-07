# employee_app/urls.py
from django.urls import path,include
from rest_framework.routers import DefaultRouter

from .views import VideoGenViewSet,DoctorVideoViewSet,EmployeeViewSet,employee_login_api,add_doctor,bulk_upload_employees,DoctorListByEmployee, DoctorVideoListView,CustomTokenRefreshView,bulk_upload_doctors,DoctorVideoGeneration,EmployeeExportExcelView,DoctorVideoExportExcelView,total_employee_count,todays_active_employees,TodaysActiveEmployeeExcelExport,doctors_with_output_video_count,doctors_with_output_video_excel,doctors_count,VideoTemplateAPIView,GenerateDoctorOutputVideoView, update_employees_from_excel,TemplateWiseVideoCountView


from rest_framework_simplejwt.views import ( # type: ignore
    TokenObtainPairView,
    TokenRefreshView,
)



router = DefaultRouter()
router.register(r'generate-video', VideoGenViewSet, basename='doctorvideo')
router.register(r'employees', EmployeeViewSet, basename='employee')
router.register(r'doctors', DoctorVideoViewSet, basename='doctorvideos')



urlpatterns = [

    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('token/refresh/', CustomTokenRefreshView.as_view(), name='token_refresh'),
    path('api/login/', employee_login_api, name='employee_login_api'),
    path('api/doctors/add/', add_doctor, name='add_doctor'),
    path('api/', include(router.urls)),
    path('api/bulk-upload-employees/', bulk_upload_employees, name='bulk_upload_employees'),
    path('api/bulk-upload-doctors/', bulk_upload_doctors, name='bulk_upload_doctor_videos'),
    path('api/by-employee/doctors/', DoctorListByEmployee.as_view(), name='doctors-by-employee'),
    path('api/by-employee/doctors-video/', DoctorVideoListView.as_view(), name='doctors_video-by-employee'),
    path('api/retry-video/doctors-video/', DoctorVideoGeneration.as_view(), name='doctors_video-by-doctor-id'),
    path('api/export-doctor-videos/', DoctorVideoExportExcelView.as_view(), name='export-doctor-videos'),
    path('api/export-employees/', EmployeeExportExcelView.as_view(), name='export-employees'),
    path('api/count_employee/', total_employee_count, name='employee_count'),
    path('api/active_today/', todays_active_employees, name='todays_active_employees'),
    path('export/active-employees/', TodaysActiveEmployeeExcelExport.as_view(), name='export-active-employees'),
    path('api/doctor_video_count/', doctors_with_output_video_count, name='doctors-output-video-count'),
    path('api/export/doctor_video/', doctors_with_output_video_excel, name='doctors-output-video-excel'),
    path('api/doctor_count/', doctors_count, name='doctors-count'),
    path('api/video-templates/', VideoTemplateAPIView.as_view(), name='video-template-list-create'),
    path('api/video-templates/<int:pk>/', VideoTemplateAPIView.as_view(), name='video-template-detail'),
    path('api/generate-doctor-video/', GenerateDoctorOutputVideoView.as_view(), name='generate-doctor-video'),
    path('api/update-from-excel/', update_employees_from_excel, name='update_employees_from_excel'),
    path('video/template-count/', TemplateWiseVideoCountView.as_view(), name='template-video-count'),

]
