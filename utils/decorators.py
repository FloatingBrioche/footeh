from functools import wraps

from flask import redirect, session, request, render_template, current_app as app
from pydantic import BaseModel, ValidationError


def login_required(f):
    """
    Decorate routes to require login.
    https://flask.palletsprojects.com/en/latest/patterns/viewdecorators/
    """

    @wraps(f)
    def wrapper(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)

    return wrapper


def validate_form(validator: BaseModel, template: str):
    """
    Decorator to validate POST request data using a Pydantic model.
    If validation fails, renders the specified template with an error message.
    """

    def provide_decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            app.logger.info("Validating registration")
            try:
                validated_data = validator(**request.form)
                return f(validated_data, *args, **kwargs)
            except ValidationError as e:
                app.logger.info("Validation failed: %s", str(e))
                return render_template(template, error_msg=str(e))

        return wrapper

    return provide_decorator
