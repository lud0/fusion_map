from django.conf import settings

from .fusion import FusionTable

fusion_table = FusionTable(credentials=settings.GOOGLE_CREDENTIALS_FILE, table_id=settings.GOOGLE_FUSIONTABLE_ID)
