import math
from google.adk.agents import Agent

import os

def read_agent_instructions()-> str:
    script_dir = os.path.dirname(os.path.abspath(__file__))
    instructions_path = os.path.join(script_dir, "instructions.txt")
    with open(instructions_path) as f:
        return f.read().strip()

def area_of_circle(radius:float)->float:
    print("AI tool for calculating area of circle")

    return math.pi * radius**2

def area_of_triangle(width:float, height:float)->float:
    return 0.5 * (width * height)

# def list_tools():
#     return tools
agent_tools = [area_of_triangle,area_of_circle]
print("Starter demo using google agent adk")

area = area_of_circle(10)
print(f"Area of circle {area}")

agent_instructions = read_agent_instructions()

root_agent = Agent(
    name="shapes_agent",
    model="gemini-2.0-flash",
    description="Agent to answer questions about Area of a cirle.",
    instruction= agent_instructions,
    tools=agent_tools
)

