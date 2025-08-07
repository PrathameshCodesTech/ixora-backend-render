from celery import shared_task
import logging
from employee_app.models import DoctorVideo, VideoTemplates, DoctorOutputVideo
from django.conf import settings
import os

logger = logging.getLogger(__name__)

@shared_task
def generate_custom_video_task(
    doctor_id,
    template_id,
    output_path,
    main_video_path,
    image_path,
    name,
    clinic,
    city,
    specialization_key,
    time_duration,
    state,
    resolution,
    base_x,
    base_y,
    line_spacing,
    overlay_x,
    overlay_y,
):
    from employee_app.views import VideoGenViewSet  # Import here to avoid circular imports
    # Create an instance just to use its method, or make the method @staticmethod if you prefer
    v = VideoGenViewSet()
    try:
        v.generate_custom_video(
            main_video_path=main_video_path,
            image_path=image_path,
            name=name,
            clinic=clinic,
            city=city,
            specialization_key=specialization_key,
            time_duration=time_duration,
            state=state,
            output_path=output_path,
            resolution=resolution,
            base_x=base_x,
            base_y=base_y,
            line_spacing=line_spacing,
            overlay_x=overlay_x,
            overlay_y=overlay_y,
        )
        relative_path = os.path.relpath(output_path, settings.MEDIA_ROOT)
        doctor = DoctorVideo.objects.get(pk=doctor_id)
        template = VideoTemplates.objects.get(pk=template_id)
        DoctorOutputVideo.objects.create(
            doctor=doctor,
            template=template,
            video_file=relative_path
        )
        logger.info("DoctorOutputVideo database record created successfully (celery task)")
    except Exception as e:
        logger.error(f"VideoGenViewSet error generating video (celery task): {e}")
        logger.error(f"Exception type: {type(e).__name__}")
