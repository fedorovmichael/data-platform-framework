from app.transformers.transform_base import Transformer


class NumericStringToIntegerTransformer(Transformer[str, int]):
    def transform(self, data: str) -> int:
        return int(data)
