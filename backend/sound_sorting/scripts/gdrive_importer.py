import json
import os
from django.core.wsgi import get_wsgi_application

os.environ['DJANGO_SETTINGS_MODULE'] = 'WebAdmin.settings'
application = get_wsgi_application()

from sound_sorting.models import SoundItem, GameFolder

with open("gdrive_data.git-exclude.json", "rb") as f:
    sound_data = json.load(f)

for local_sound_path, gdrive_id in sound_data.items():
    site_path = local_sound_path.replace("sound_sorting/", "")
    print(site_path)
    if gdrive_id:
        dir_path = os.path.dirname(site_path)
        file_name = os.path.basename(site_path)
        f = GameFolder.get_folder_by_path(dir_path)
        sf, _ = SoundItem.objects.get_or_create(name=file_name, parent_folder=f)
        sf.gdrive_id = gdrive_id
        sf.save()
