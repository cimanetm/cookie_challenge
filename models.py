from django.db import models
from django.contrib.auth.hashers import make_password

class User(models.Model):
    ROLE_CHOICES = [
        ('baker', 'Baker'),
        ('voter', 'Voter'),
    ]

    username = models.CharField(max_length=150, unique=True)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=128)  # Store hashed passwords
    role = models.CharField(max_length=10, choices=ROLE_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        # Automatically hash the password before saving if not already hashed
        if not self.password.startswith('pbkdf2_'):  # Example prefix for Django's default hasher
            self.password = make_password(self.password)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.username

# Recipe model
class Recipe(models.Model):
    baker = models.ForeignKey(User, on_delete=models.CASCADE, related_name='recipes')
    title = models.CharField(max_length=255)
    description = models.TextField()
    ingredients = models.TextField()  # Store ingredients as plain text or JSON
    instructions = models.TextField()
    image = models.ImageField(upload_to='recipe_images/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

# Vote model
class Vote(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE, related_name='votes')
    voter = models.ForeignKey(User, on_delete=models.CASCADE, related_name='votes')
    proof_image = models.ImageField(upload_to='proof_images/')
    submitted_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('recipe', 'voter')  # Ensure one vote per voter per recipe

    def __str__(self):
        return f"Vote by {self.voter.username} for {self.recipe.title}"

# Result model (optional for leaderboard)
class Result(models.Model):
    recipe = models.OneToOneField(Recipe, on_delete=models.CASCADE, related_name='result')
    votes_count = models.PositiveIntegerField(default=0)
    declared_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Result for {self.recipe.title}: {self.votes_count} votes"
