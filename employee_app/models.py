from django.db import models
from django.utils import timezone
import os

class Employee(models.Model):
    USER_TYPE_CHOICES = [
        ('Employee', 'Employee'),
        ('Admin', 'Admin'),
        ('SuperAdmin', 'SuperAdmin'),
    ]

    employee_id = models.CharField(max_length=10, unique=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100, null=True, blank=True)
    email = models.EmailField(unique=True, null=True, blank=True)
    phone = models.CharField(max_length=15, null=True, blank=True)
    department = models.CharField(max_length=100, null=True, blank=True)
    date_joined = models.DateField(auto_now_add=True)
    user_type = models.CharField(max_length=20, choices=USER_TYPE_CHOICES, default='Employee')
    status = models.BooleanField(default=True)
    login_date = models.DateTimeField(default=timezone.now)
    rbm = models.ForeignKey(
        'self',                   # Self-referential
        on_delete=models.SET_NULL,  # Prefer SET_NULL to avoid cascade delete
        null=True,
        blank=True,
        related_name='team_members'  # Optional reverse relation
    )
    city = models.CharField(max_length=30,blank=True, null=True)
    has_logged_in = models.BooleanField(default=False)  
    
    def __str__(self):
        return f"{self.first_name} {self.last_name}"
    


class EmployeeLoginHistory(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='login_history')
    
    # Snapshot fields (renamed to avoid conflict)
    employee_identifier = models.CharField(max_length=10,null=True, blank=True)  # Was employee_id
    name = models.CharField(max_length=200,null=True, blank=True)
    email = models.EmailField(null=True, blank=True)
    phone = models.CharField(max_length=15, null=True, blank=True)
    department = models.CharField(max_length=100, null=True, blank=True)
    user_type = models.CharField(max_length=20,null=True, blank=True)
    login_time = models.DateTimeField(default=timezone.now,null=True, blank=True)

    def __str__(self):
        return f"{self.name} logged in at {self.login_time}"


class DoctorVideo(models.Model):
    name = models.CharField(max_length=285)
    designation = models.CharField(max_length=255)
    clinic = models.CharField(max_length=255)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100, null=True, blank=True)
    image = models.ImageField(upload_to='doctor_images/')
    specialization = models.CharField(max_length=255)
    specialization_key = models.CharField(max_length=255, null=True, blank=True)
    mobile_number = models.CharField(max_length=15)
    whatsapp_number = models.CharField(max_length=15)
    description = models.TextField()
    output_video = models.FileField(upload_to='output/', null=True, blank=True)
    created_at = models.DateTimeField(default=timezone.now)

    employee = models.ForeignKey(Employee,  on_delete=models.CASCADE, related_name='doctors_video',null=True, blank=True)

    def __str__(self):
        return self.name
    

class Doctor(models.Model):
    name = models.CharField(max_length=255)
    designation = models.CharField(max_length=255)
    clinic = models.CharField(max_length=255)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100,null=True, blank=True)
    image = models.ImageField(upload_to='doctor_images/', blank=True, null=True)
    specialization = models.CharField(max_length=255)
    mobile_number = models.CharField(max_length=15)
    whatsapp_number = models.CharField(max_length=15)
    description = models.TextField()
    output_video = models.FileField(upload_to='doctor_videos/', blank=True, null=True)
    employee = models.ForeignKey(Employee,  on_delete=models.CASCADE, related_name='doctors',null=True, blank=True)

    def __str__(self):
        return f"{self.name} - {self.specialization}"

@property
def video_url(self):
    if self.output_video:
        return f"https://vibecopilot.ai{self.output_video.url}"
    return None


class VideoTemplates(models.Model):
    
    name = models.CharField(max_length=100,null=True, blank=True)
    template_video = models.FileField(upload_to='video-template/')
    base_x_axis = models.CharField(max_length=100,null=True, blank=True)
    base_y_axis = models.CharField(max_length=100,null=True, blank=True)
    overlay_x = models.CharField(max_length=100,null=True, blank=True)
    overlay_y = models.CharField(max_length=100,null=True, blank=True)
    time_duration = models.CharField(max_length=100,null=True, blank=True)
    line_spacing = models.CharField(max_length=100,null=True, blank=True)
    resolution = models.CharField(max_length=100,null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.BooleanField(default=True)
    
    def __str__(self):
        return f"Video for {self.template_video}"



# def doctor_video_upload_path(instance, filename):
#     employee_id = instance.doctor.employee.id if instance.doctor and instance.doctor.employee else 'unknown_employee'
#     doctor_id = instance.doctor.id if instance.doctor else 'unknown_doctor'
#     # template_id = instance.template.id if instance.template else 'unknown_template'

#     return os.path.join('output', str(employee_id), str(doctor_id),filename)

def doctor_video_upload_path(instance, filename):
    employee_id = (
        instance.doctor.employee.id 
        if instance.doctor and hasattr(instance.doctor, 'employee') and instance.doctor.employee 
        else 'unknown_employee'
    )
    doctor_id = instance.doctor.id if instance.doctor else 'unknown_doctor'
    return os.path.join('output', str(employee_id), str(doctor_id), filename)

class DoctorOutputVideo(models.Model):

    doctor = models.ForeignKey(DoctorVideo, on_delete=models.CASCADE, null=True, blank=True)
    template = models.ForeignKey(VideoTemplates, on_delete=models.SET_NULL,null=True,blank=True)
    video_file = models.FileField(upload_to=doctor_video_upload_path)
    created_at = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return f"Video for {self.doctor_video.name} - {self.id}"





