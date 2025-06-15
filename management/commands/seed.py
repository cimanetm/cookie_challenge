import random
from datetime import datetime, timedelta
from faker import Faker

from django.core.management.base import BaseCommand
 
from cookie_challenge.models import *

fake = Faker()

# Predefined cookie recipes
COOKIE_RECIPES = [
    {
        "title": "Classic Chocolate Chip Cookies",
        "description": "A timeless favorite, perfect for any occasion.",
        "ingredients": "2 1/4 cups all-purpose flour, 1 tsp baking soda, 1 tsp salt, 1 cup butter, 3/4 cup sugar, 3/4 cup brown sugar, 1 tsp vanilla extract, 2 large eggs, 2 cups semi-sweet chocolate chips.",
        "instructions": "1. Preheat oven to 375°F. 2. Combine flour, baking soda, and salt in a small bowl. 3. Beat butter, sugar, brown sugar, and vanilla in a large bowl. 4. Add eggs, one at a time, beating well. 5. Gradually add flour mixture. 6. Stir in chocolate chips. 7. Drop by spoonfuls onto ungreased baking sheets. 8. Bake for 9–11 minutes.",
    },
    {
        "title": "Oatmeal Raisin Cookies",
        "description": "Chewy and soft, these cookies are a wholesome treat.",
        "ingredients": "1 3/4 cups flour, 1 tsp baking soda, 1/2 tsp salt, 1 cup butter, 1 cup brown sugar, 1/2 cup sugar, 2 large eggs, 1 tsp vanilla, 3 cups rolled oats, 1 cup raisins.",
        "instructions": "1. Preheat oven to 350°F. 2. Mix flour, baking soda, and salt. 3. Cream butter, sugar, and brown sugar. 4. Add eggs and vanilla. 5. Gradually mix in dry ingredients. 6. Fold in oats and raisins. 7. Drop spoonfuls onto baking sheets. 8. Bake for 10–12 minutes.",
    },
    {
        "title": "Peanut Butter Cookies",
        "description": "Rich and nutty, these cookies melt in your mouth.",
        "ingredients": "1 cup peanut butter, 1 cup sugar, 1 large egg, 1 tsp vanilla extract.",
        "instructions": "1. Preheat oven to 350°F. 2. Mix all ingredients in a bowl. 3. Roll into balls and place on a baking sheet. 4. Flatten with a fork in a criss-cross pattern. 5. Bake for 8–10 minutes.",
    },
]

class Command(BaseCommand):
    help = "Seed the database with cookie-related data for testing, including votes and results."

    def handle(self, *args, **kwargs):
        # Clear existing data
        User.objects.all().delete()
        Recipe.objects.all().delete()
        Vote.objects.all().delete()
        Result.objects.all().delete()

        self.stdout.write("Seeding database with cookie recipes, votes, and results...")

        # Create bakers
        bakers = [
            User.objects.create(
                username=fake.unique.user_name(),
                email=fake.unique.email(),
                password="password123",  # Password is hashed automatically
                role="baker"
            )
            for _ in range(len(COOKIE_RECIPES))
        ]

        # Create voters
        voters = [
            User.objects.create(
                username=fake.unique.user_name(),
                email=fake.unique.email(),
                password="password123",  # Password is hashed automatically
                role="voter"
            )
            for _ in range(20)  # Create 20 voters
        ]

        # Create recipes
        recipes = []
        for baker, cookie in zip(bakers, COOKIE_RECIPES):
            recipe = Recipe.objects.create(
                baker=baker,
                title=cookie["title"],
                description=cookie["description"],
                ingredients=cookie["ingredients"],
                instructions=cookie["instructions"],
                created_at=fake.date_time_between(start_date="-1y", end_date="now"),
            )
            recipes.append(recipe)

        # Generate votes
        for voter in voters:
            voted_recipes = random.sample(recipes, random.randint(1, len(recipes)))  # Each voter votes on 1 to all recipes
            for recipe in voted_recipes:
                if not Vote.objects.filter(recipe=recipe, voter=voter).exists():  # Avoid duplicate votes
                    Vote.objects.create(
                        recipe=recipe,
                        voter=voter,
                        proof_image=fake.image_url(),  # Placeholder image URL
                        submitted_at=fake.date_time_between(start_date=recipe.created_at, end_date="now"),
                    )

        # Calculate and save results
        for recipe in recipes:
            vote_count = Vote.objects.filter(recipe=recipe).count()
            Result.objects.create(
                recipe=recipe,
                votes_count=vote_count,
            )

        self.stdout.write(self.style.SUCCESS("Seeding complete with recipes, votes, and results!"))
