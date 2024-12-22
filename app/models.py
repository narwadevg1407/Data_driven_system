from django.db import models
from django.contrib.auth.models import User


class Folders(models.Model):
    folder_name = models.CharField(max_length=100)
    parent = models.ForeignKey("self", on_delete=models.CASCADE, null=True, blank=True, related_name="subfolders")
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    def get_full_path(self):
        """
        Recursively get the full path of the folder
        """
        if self.parent:
            return f"{self.parent.get_full_path()}/{self.name}"
        return self.name

    def __str__(self):
        return self.folder_name

    class Meta:
        unique_together = ('folder_name', 'parent', 'user_id')
        ordering = ['folder_name']


class Files(models.Model):
    file_name = models.CharField(max_length=100)
    file = models.FileField(upload_to="files/")
    folder = models.ForeignKey(Folders, on_delete=models.CASCADE, null=True, blank=True, related_name="files")
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def get_absolute_url(self):
        """
        Generate a URL for direct file access
        """
        return f"{self.file.url}"

    def __str__(self):
        return self.file_name

    class Meta:
        unique_together = ('file_name', 'folder', 'user_id')
        ordering = ['file_name']




