from typing import Dict, List

from core.models import Recipe, Tag


def get_or_create_tags_for_recipe(recipe: Recipe, tags: List[Dict[str, str]]):
    for tag in tags:
        tag_obj, _ = Tag.objects.get_or_create(
            user=recipe.user,
            **tag,
        )

        recipe.tags.add(tag_obj)
