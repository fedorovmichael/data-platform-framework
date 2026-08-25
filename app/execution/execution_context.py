from dataclasses import dataclass
from typing import Any


@dataclass(slots=True)
class ExecutionContext:
    execution_id: str
    resources: dict[str, Any]

    def get_resource(self, name: str) -> Any:
        if name not in self.resources:
            raise RuntimeError(f"Execution resource '{name}' is not available.")

        return self.resources[name]