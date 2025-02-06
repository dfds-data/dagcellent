"""
This type stub file was generated by pyright.
"""

from flask_appbuilder.fieldwidgets import BS3TextAreaFieldWidget, BS3TextFieldWidget
from flask_appbuilder.widgets import RenderTemplateWidget

class AirflowModelListWidget(RenderTemplateWidget):
    """Airflow model list."""

    template = ...

class AirflowDateTimePickerWidget:
    """Airflow date time picker widget."""

    data_template = ...
    def __call__(self, field, **kwargs):  # -> Markup:
        ...

class AirflowDateTimePickerROWidget(AirflowDateTimePickerWidget):
    """Airflow Read-only date time picker widget."""

    def __call__(self, field, **kwargs):  # -> Markup:
        ...

class BS3TextFieldROWidget(BS3TextFieldWidget):
    """Read-only single-line text input Widget (BS3TextFieldWidget)."""

    def __call__(self, field, **kwargs):  # -> Markup:
        ...

class BS3TextAreaROWidget(BS3TextAreaFieldWidget):
    """Read-only multi-line text area Widget (BS3TextAreaROWidget)."""

    def __call__(self, field, **kwargs):  # -> Markup:
        ...

class AirflowVariableShowWidget(RenderTemplateWidget):
    """Airflow variable show widget."""

    template = ...
