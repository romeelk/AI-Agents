from datetime import datetime
import json
from random import randint
from typing import Any, Callable, Set

def create_user_story(name:str,description: str) -> str:
    """
    Simulates creating a user story in a app like Jira or ADO
    :param description: A description of the user story
    :return: Story information with JSON string.
    """
    story_id = randint(1,100)
    story_json =  json.dumps({
        "id": story_id,
        "name": name,
        "description": description,
        "created": datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    })
    return story_json

user_functions : Set[Callable[..., Any]] = {
    create_user_story
}