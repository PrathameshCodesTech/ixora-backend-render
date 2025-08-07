from rest_framework import serializers
from .models import Doctor,Employee,DoctorVideo,VideoTemplates,DoctorOutputVideo


class EmployeeLoginSerializer(serializers.Serializer):
    employee_id = serializers.CharField()
    

class EmployeeSerializer(serializers.ModelSerializer):
    rbm_name = serializers.SerializerMethodField()

    class Meta:
        model = Employee
        fields = '__all__'
        read_only_fields = ['rbm_name']

    def get_rbm_name(self, obj):
        if obj.rbm:
            return f"{obj.rbm.first_name} {obj.rbm.last_name or ''}".strip()
        return None
    

class DoctorSerializer(serializers.ModelSerializer):
    image = serializers.ImageField(required=False, allow_null=True)  # Handle image field if null
   
    class Meta:
        model = DoctorVideo
        fields = ['id', 'name', 'designation', 'clinic', 'city', 'state', 'image', 'specialization', 'mobile_number', 'whatsapp_number', 'description', 'output_video', 'employee']


class DoctorOutputVideoSerializer(serializers.ModelSerializer):

    class Meta:
        model = DoctorOutputVideo
        fields = '__all__'


class DoctorVideoSerializer(serializers.ModelSerializer):
    image = serializers.ImageField(required=False, allow_null=True)
    latest_output_video = serializers.SerializerMethodField()
    employee_name = serializers.SerializerMethodField()
    rbm_name = serializers.SerializerMethodField()
    # employee_designation = serializers.SerializerMethodField()  # ✅ New field

    class Meta:
        model = DoctorVideo
        fields = [
            'id', 'name', 'designation', 'clinic', 'city', 'state',
            'image', 'specialization', 'specialization_key',
            'mobile_number', 'whatsapp_number', 'description',
            'output_video', 'created_at', 'employee',
            'latest_output_video', 'employee_name', 'rbm_name',
            
        ]

    def get_latest_output_video(self, obj):
        videos = DoctorOutputVideo.objects.filter(doctor=obj).order_by('-id')
        return DoctorOutputVideoSerializer(videos, many=True).data

    def get_employee_name(self, obj):
        if obj.employee:
            return f"{obj.employee.first_name} {obj.employee.last_name}".strip()
        return None

    def get_rbm_name(self, obj):
        if obj.employee and obj.employee.rbm:
            return f"{obj.employee.rbm.first_name} {obj.employee.rbm.last_name}".strip()
        return None

    # def get_employee_designation(self, obj):
    #     if obj.employee and obj.employee.designation:
    #         return obj.employee.designation
    #     return None


class VideoTemplatesSerializer(serializers.ModelSerializer):

    class Meta:
        model = VideoTemplates
        fields = '__all__'


