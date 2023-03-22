from django.db import models
from myauth.models import UserProfile


def get_folder_full_path(folder):
    parent_folders = [folder.name]
    while True:
        # get parent folder from folder, check if not set as null
        folder = folder.parent_folder
        if folder:
            parent_folders.append(folder.name)
        else:
            break
    return "/".join(reversed(parent_folders)) + "/"


def get_sound_upload_dest(instance, filename):
    # get parent folder full path from sound
    folder_full_path = get_folder_full_path(instance.parent_folder)
    return f"sound_sorting/{folder_full_path}{instance.name}"


class GameFolder(models.Model):
    GAME_TYPE = "REAL"

    name = models.CharField(max_length=50)
    # field for separating into categories, eg, real game folders and "Bounties" folder with "wanted" sounds
    type = models.CharField(max_length=6, default=GAME_TYPE)
    parent_folder = models.ForeignKey('self', on_delete=models.SET_NULL,
                                      null=True, blank=True, related_name="child_folders")

    class Meta:
        unique_together = ('name', 'parent_folder')
        ordering = ('name',)

    def __str__(self):
        return get_folder_full_path(self)

    @staticmethod
    def get_folder_by_path(folder_path):
        folders = folder_path.split("/")
        parent_folder = None
        f = None

        for folder in folders:
            f, _ = GameFolder.objects.get_or_create(name=folder, parent_folder=parent_folder)
            parent_folder = f
        return f


class SoundItem(models.Model):
    likes = models.IntegerField(default=0)
    dislikes = models.IntegerField(default=0)

    name = models.CharField(max_length=200)
    parent_folder = models.ForeignKey(GameFolder, on_delete=models.CASCADE, related_name="child_sounds")
    gdrive_id = models.CharField(max_length=50)

    class Meta:
        unique_together = ('name', 'parent_folder')
        ordering = ('-id',)

    def __str__(self):
        return get_sound_upload_dest(self, "")

    def update_like_dislike_amount(self):
        self.likes = SoundItemReview.objects.filter(sound=self, is_useful=True).count()
        self.dislikes = SoundItemReview.objects.filter(sound=self, is_useful=False).count()
        self.save()


class SoundCategory(models.Model):
    name = models.CharField(max_length=200, unique=True)

    def __str__(self):
        return self.name


class SoundItemReview(models.Model):
    sound = models.ForeignKey(SoundItem, on_delete=models.CASCADE, related_name='sound_reviews')
    user_profile = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name="sound_reviews")
    is_useful = models.BooleanField(null=True, blank=True)
    categories = models.ManyToManyField(SoundCategory, related_name="sound_reviews", blank=True)
    text_review = models.TextField(max_length=50, blank=True)

    created_ts = models.DateTimeField(auto_now_add=True)
    updated_ts = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('user_profile', 'sound')

    def __str__(self):
        return f"{self.user_profile.user}: {self.sound}"
