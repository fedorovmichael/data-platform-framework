from app.transformers.transform_base import Transformer
from typing import Optional


class NumericStringToIntegerTransformer(Transformer[str, Optional[int]]):
    def transform(self, data: str) -> Optional[int]:
        return int(data)