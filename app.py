import os
import sys
import solara

from matplotlib.markers import MarkerStyle

sys.path.insert(0, os.path.abspath("../../../.."))

from model import BoidFlockers
#from mesa.examples.basic.boid_flockers.model import BoidFlockers
from model import BoidFlockers
from mesa.visualization import Slider, SolaraViz, make_space_component

# Pre-compute markers for different angles (e.g., every 10 degrees)
MARKER_CACHE = {}
for angle in range(0, 360, 10):
    marker = MarkerStyle(10)
    marker._transform = marker.get_transform().rotate_deg(angle)
    MARKER_CACHE[angle] = marker


def boid_draw(agent):
    neighbors = len(agent.neighbors)

    # Calculate the angle
    deg = agent.angle
    # Round to nearest 10 degrees
    rounded_deg = round(deg / 10) * 10 % 360

    # using cached markers to speed things up
    if neighbors <= 1:
        return {"color": "red", "size": 20, "marker": MARKER_CACHE[rounded_deg]}
    elif neighbors >= 2:
        return {"color": "green", "size": 20, "marker": MARKER_CACHE[rounded_deg]}


model_params = {
    "seed": {
        "type": "InputText",
        "value": 42,
        "label": "Random Seed",
    },
    "population_size": Slider(
        label="Number of boids",
        value=100,
        min=10,
        max=200,
        step=10,
    ),
    "width": 100,
    "height": 100,
    "speed": Slider(
        label="Speed of Boids",
        value=5,
        min=1,
        max=20,
        step=1,
    ),
    "vision": Slider(
        label="Vision of Bird (radius)",
        value=10,
        min=1,
        max=50,
        step=1,
    ),
    "separation": Slider(
        label="Minimum Separation",
        value=2,
        min=1,
        max=20,
        step=1,
    ),
}

model = BoidFlockers()

# Convert to a Solara component
def heading_display(model):
    return solara.Text(f"Heading: {model.average_heading}, Delta {model.delta_average_heading}")

page = SolaraViz(
    model,
    components=[heading_display, make_space_component(agent_portrayal=boid_draw, backend="matplotlib")],
    model_params=model_params,
    name="Boid Flocking Model",
)

page  # noqa
