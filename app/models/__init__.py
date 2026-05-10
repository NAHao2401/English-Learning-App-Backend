"""Model package initializer: import submodules so all ORM models are registered.

Importing submodules here ensures SQLAlchemy's DeclarativeBase registry
knows about all model classes when the package is imported (prevents
forward-reference errors for relationships declared with string names).
"""

from . import lesson  # noqa: F401
from . import vocabulary  # noqa: F401
from . import progress  # noqa: F401
from . import user  # noqa: F401
from . import user_vocabulary  # noqa: F401
