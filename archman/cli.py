#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import typer
import json
from typing import Optional
from uuid import UUID
from rich.console import Console
from rich.table import Table

from .models import Component, System, ComponentType
from .services import ComponentService, SystemService

app = typer.Typer()
console = Console()
component_service = ComponentService()
system_service = SystemService()


# Component commands
@app.command("add-component")
def add_component(
    name: str = typer.Option(..., help="Name of the component"),
    type: ComponentType = typer.Option(
        ..., help="Type of component (hardware, software, database, people, process)"
    ),
    properties: str = typer.Option("{}", help="JSON string of properties"),
):
    """Add a new component to the architecture."""
    try:
        props = json.loads(properties)
        component = Component(name=name, type=type, properties=props)
        result = component_service.create_or_update(component)
        console.print(f"Component created with UUID: {result.uuid}", style="green")
    except Exception as e:
        console.print(f"Error: {str(e)}", style="red")


@app.command("list-components")
def list_components(
    type: Optional[ComponentType] = typer.Option(None, help="Filter by component type")
):
    """List all components or filter by type."""
    try:
        if type:
            components = component_service.get_by_type(type)
        else:
            components = component_service.get_all()

        table = Table("UUID", "Name", "Type", "Properties")
        for comp in components:
            table.add_row(
                str(comp.uuid),
                comp.name,
                comp.type,
                json.dumps(comp.properties, indent=2),
            )
        console.print(table)
    except Exception as e:
        console.print(f"Error: {str(e)}", style="red")


# System commands
@app.command("add-system")
def add_system(
    name: str = typer.Option(..., help="Name of the system"),
    properties: str = typer.Option("{}", help="JSON string of properties"),
):
    """Add a new system to the architecture."""
    try:
        props = json.loads(properties)
        system = System(name=name, properties=props)
        result = system_service.create_or_update(system)
        console.print(f"System created with UUID: {result.uuid}", style="green")
    except Exception as e:
        console.print(f"Error: {str(e)}", style="red")


@app.command("list-systems")
def list_systems():
    """List all systems."""
    try:
        systems = system_service.get_all()

        table = Table("UUID", "Name", "Component Count", "Properties")
        for sys in systems:
            table.add_row(
                str(sys.uuid),
                sys.name,
                str(len(sys.components)),
                json.dumps(sys.properties, indent=2),
            )
        console.print(table)
    except Exception as e:
        console.print(f"Error: {str(e)}", style="red")


@app.command("add-component-to-system")
def add_component_to_system(
    system_uuid: UUID = typer.Option(..., help="UUID of the system"),
    component_uuid: UUID = typer.Option(..., help="UUID of the component to add"),
):
    """Add a component to a system."""
    try:
        result = system_service.add_component_to_system(system_uuid, component_uuid)
        if result:
            console.print(
                f"Component {component_uuid} added to system {system_uuid}",
                style="green",
            )
        else:
            console.print("System or component not found", style="red")
    except Exception as e:
        console.print(f"Error: {str(e)}", style="red")


@app.command("show-system")
def show_system(uuid: UUID = typer.Option(..., help="UUID of the system to show")):
    """Show details of a system including its components."""
    try:
        system = system_service.get_full_system(uuid)
        if not system:
            console.print("System not found", style="red")
            return

        console.print(f"System: {system.name} ({system.uuid})")
        console.print(f"Properties: {json.dumps(system.properties, indent=2)}")

        if system.components:
            table = Table("UUID", "Name", "Type", "Properties")
            for comp in system.components:
                table.add_row(
                    str(comp.uuid),
                    comp.name,
                    comp.type,
                    json.dumps(comp.properties, indent=2),
                )
            console.print("Components:")
            console.print(table)
        else:
            console.print("No components in this system")
    except Exception as e:
        console.print(f"Error: {str(e)}", style="red")


if __name__ == "__main__":
    app()
