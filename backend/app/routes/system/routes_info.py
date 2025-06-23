from fastapi import FastAPI, APIRouter, Request
from fastapi.routing import APIRoute
from typing import Any, Dict, List, Type, Union, get_args, get_origin
from pydantic import BaseModel
from enum import Enum

router = APIRouter()

PY_TO_JS_TYPE = {
    "str": "string",
    "int": "number",
    "float": "number",
    "bool": "boolean",
    "datetime.datetime": "string",
    "uuid.UUID": "string",
    "pydantic.networks.EmailStr": "string",
    "EmailStr": "string",
    "decimal.Decimal": "string",
    "NoneType": "null",
    "Any": "any",
}


def python_type_to_js(type_: Any) -> str:
    """
    Converts a Python type annotation into a JS-friendly type string.
    Supports Optional, List, Dict, Union, Enum, etc.
    """
    origin = get_origin(type_)
    args = get_args(type_)

    if origin is Union:
        subtypes = [python_type_to_js(arg) for arg in args]
        return " | ".join(sorted(set(subtypes)))

    elif origin in (list, List):
        inner = python_type_to_js(args[0]) if args else "any"
        return f"{inner}[]"

    elif origin in (dict, Dict):
        return "Record<string, any>"

    elif isinstance(type_, type) and issubclass(type_, Enum):
        # Return all enum values as a union of strings
        return " || ".join(f'"{item.value}"' for item in type_)

    elif isinstance(type_, type):
        return PY_TO_JS_TYPE.get(type_.__name__, type_.__name__)

    elif hasattr(type_, "__name__"):
        return PY_TO_JS_TYPE.get(type_.__name__, type_.__name__)

    return "any"

def extract_schema_fields(schema: Type[BaseModel]) -> Dict[str, Any]:
    """
    Recursively extracts a dictionary of {field_name: JS_type or nested_fields}
    from a Pydantic schema, including nested BaseModels.
    """
    fields = {}
    for name, field in schema.model_fields.items():
        js_type = python_type_to_js(field.annotation)
        fields[name] = js_type
    return fields


def get_routes_with_schemas(app: FastAPI) -> List[Dict[str, Any]]:
    """
    Scans all FastAPI routes and extracts path, method, input/output schemas,
    and their field definitions (recursively resolved).
    """
    result = []

    for route in app.routes:
        if not isinstance(route, APIRoute):
            continue

        route_data = {
            "path": route.path,
            "methods": list(route.methods - {"HEAD", "OPTIONS"}),
            "name": route.name,
            "summary": route.summary,
            "tags": route.tags,
            "input_schema": None,
            "schema_fields": None,
            "output_schema": None,
            "output_schema_fields": None,
        }

        # Try extracting input schema from meta
        meta = getattr(route.endpoint, "_meta", {})
        schema_class = meta.get("input_schema")

        # Fallback to body param
        if schema_class is None:
            for param in route.dependant.body_params:
                if isinstance(param.type_, type) and issubclass(param.type_, BaseModel):
                    schema_class = param.type_
                    break

        if schema_class and issubclass(schema_class, BaseModel):
            route_data["input_schema"] = schema_class.__name__
            route_data["schema_fields"] = extract_schema_fields(schema_class)

        # Output schema
        response_model = getattr(route, "response_model", None)
        if isinstance(response_model, type) and issubclass(response_model, BaseModel):
            route_data["output_schema"] = response_model.__name__
            route_data["output_schema_fields"] = extract_schema_fields(response_model)

        print(f"{route.name}: response_model = {response_model}")

        result.append(route_data)

    return result


@router.get("/routes-info", tags=["System"])
def get_routes_info(request: Request):
    """
    Returns metadata about all API routes, including input/output schemas and their fields,
    with full recursion for nested models.
    """
    return get_routes_with_schemas(request.app)
