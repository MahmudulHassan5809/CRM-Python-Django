from django.db import models
import uuid
# Create your models here.
class Branch(models.Model):
    branch_name = models.CharField(max_length=200)
    # parent = models.ForeignKey('self', related_name='children', on_delete=models.CASCADE, null=True, blank=True)
    # user = models.ManyToManyField('accounts.User',related_name='user_branch')


    class Meta:
        verbose_name = 'Branch'
        verbose_name_plural = '1. Branch'

    def __str__(self):
        return self.branch_name
        # full_path = [self.branch_name]
        # k = self.parent
        # while k is not None:
        #     full_path.append(k.branch_name)
        #     k = k.parent
        # return ' -> '.join(full_path[::-1])
