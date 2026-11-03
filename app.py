"""Small web interface and JSON API for the functions in target.py."""

import math
import os
from typing import Any

from flask import Flask, jsonify, render_template, request

import target

app = Flask(__name__)

FUNCTIONS = {
    "is_adult": target.is_adult,
    "celsius_to_fahrenheit": target.celsius_to_fahrenheit,
    "count_vowels": target.count_vowels,
    "invert": target.invert,
    "greet": target.greet,
    "find_max": target.find_max,
    "get_price": target.get_price,
    "swap": target.swap,
    "common_items": target.common_items,
    "is_leap_year": target.is_leap_year,
    "to_int": target.to_int,
    "divide": target.divide,
    "power": target.power,
    "square_root": target.square_root,
    "factorial": target.factorial,
    "average": target.average,
}


def json_safe(value: Any) -> Any:
    """Convert values such as sets and tuples into JSON-compatible values.

    Complex numbers and non-finite floats (inf, nan) have no valid JSON form,
    so they are shown as text instead of breaking the response.
    """
    if isinstance(value, complex) or (
        isinstance(value, float) and not math.isfinite(value)
    ):
        return str(value)
    if isinstance(value, (set, tuple)):
        converted = [json_safe(item) for item in value]
        return sorted(converted, key=repr) if isinstance(value, set) else converted
    if isinstance(value, list):
        return [json_safe(item) for item in value]
    if isinstance(value, dict):
        return {str(key): json_safe(item) for key, item in value.items()}
    return value


@app.get("/")
def index():
    return render_template("index.html", function_names=list(FUNCTIONS))


@app.get("/health")
def health():
    """Expose the SHA of the code currently running on the deployment host."""
    commit_sha = os.getenv("RENDER_GIT_COMMIT") or os.getenv("GITHUB_SHA") or "local"
    return jsonify(status="ok", commit_sha=commit_sha)


@app.post("/api/run")
def run_function():
    payload = request.get_json(silent=True)
    if not isinstance(payload, dict):
        return jsonify(error="Request body must be a JSON object."), 400

    function_name = payload.get("function")
    args = payload.get("args", [])
    kwargs = payload.get("kwargs", {})

    if function_name not in FUNCTIONS:
        return jsonify(error="Choose one of the 16 available functions."), 400
    if not isinstance(args, list) or not isinstance(kwargs, dict):
        return jsonify(error="'args' must be a JSON array and 'kwargs' must be a JSON object."), 400

    try:
        # JSON has no set type, so accept arrays for the set-based function
        # and convert them to Python sets before calling target.py.
        if function_name == "common_items":
            args = [set(arg) if isinstance(arg, list) else arg for arg in args]

        result = FUNCTIONS[function_name](*args, **kwargs)
        return jsonify(function=function_name, result=json_safe(result), result_type=type(result).__name__)
    except Exception as exc:  # noqa: BLE001 - the UI intentionally shows the target's errors
        return jsonify(function=function_name, error=type(exc).__name__, message=str(exc)), 400


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", "5000")), debug=False)
