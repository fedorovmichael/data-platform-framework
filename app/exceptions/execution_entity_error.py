class ExecutionEntityError(Exception):
    def __init__(
        self,
        entity_name: str,
        execution_id: str,
        message: str,
        cause: Exception | None = None,
    ):
        super().__init__(message)
        self.entity_name = entity_name
        self.execution_id = execution_id
        self.message = message
        self.cause = cause
