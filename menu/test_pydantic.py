from __future__ import annotations
from typing import List
from pydantic import BaseModel, ValidationError, Field, validator
    


# class Slider(BaseMenu):
#     max_value: int 
#     value: int 

# class Turner(BaseMenu):
#     value: int
#     values: list[str]


MENU_JSON = """{
    "name" : "Menu",
    "nodeType": "Menu",
    "nodes" :[
        {   
            "name" : "Start",
            "nodeType": "button",
            "nodes" : []
        },
        {   
            "name" : "Options",
            "nodeType": "Menu",
            "nodes" : [
                {   
                    "name" : "Volume",
                    "nodeType": "Slider",
                    "maxValue" : 20,
                    "value": 10,
                    "nodes" : []
                },
                {   
                    "name" : "Music",
                    "nodeType": "Turner",
                    "value": 0,
                    "values": ["hello", "my", "friend"],
                    "nodes" : []
                },
                {   
                    "name" : "Credits",
                    "nodeType": "Menu",
                    "nodes" : [
                                    {   
                                "name" : "Made by Sasha and Petya",
                                "nodeType": "Menu",
                                "nodes" : []
                            }
                    ]
                }
            ]
        },
        {   
            "name" : "Credits",
            "nodeType": "Text",
            "text" : "Hello",
            "nodes" : []
        }
    ]
}"""


menu = BaseMenu.parse_raw(
            MENU_JSON
        )

def func(node):
    if node.name == "Made by Sasha and Petya":
        node.name = "NOT"
    return node


def interate_in_menu(menu):
    
    return menu

# print(interate_in_menu(menu, func).json())
exit()
try:
    menu = BaseMenu.parse_raw(
            MENU_JSON
        )
    print(menu.json())
except ValidationError as e:
    print(e.json())

exit()









class Tag(BaseModel):
    id: int 
    tag: str

class City(BaseModel):
    city_id: int 
    name: str 
    tags: list[Tag]


input_json = """
{
    "city_id" : "132", 
    "name":"Moscow",  
    "tags": [
        { "id": 1 , "tag": "Capital" },
        { "id": 2 , "tag": "big City" }
    ]
}"""
try:
    city = City.parse_raw(
        input_json
    )
except ValidationError as e:
    print(e.json())

city = City.parse_raw(
        input_json
    )

print(city)
print(city.name)