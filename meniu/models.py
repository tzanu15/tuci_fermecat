from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Dish(models.Model):
    """
    Model representing a dish.
    """
    name = models.CharField(max_length=200)
    description = models.TextField()
    image = models.ImageField(upload_to='dishes/', blank=True, null=True)
    publication_date = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    def vote_count(self):
        """
        Returns the number of votes for this dish.
        """
        return self.vote_set.count()

class Vote(models.Model):
    """
    Model representing a user's vote for a dish.
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    dish = models.ForeignKey(Dish, on_delete=models.CASCADE)
    vote_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'dish')  # A user can only vote for a dish once

    def __str__(self):
        return f"{self.user.username} voted for {self.dish.name}"