from typing import Any, Optional, Callable, final

import pandas as pd
import pandera as pa

from pandakeeper.node import Node
from pandakeeper.typing import PD_READ_PICKLE_ANNOTATION
from pandakeeper.validators import AnyDataFrame

__all__ = (
    'DataLoader',
    'StaticDataLoader',
    'PickleLoader'
)


class DataLoader(Node):
    __slots__ = ('__loader', '__loader_args', '__loader_kwargs')

    def __init__(self,
                 loader: Callable[..., pd.DataFrame],
                 *loader_args: Any,
                 output_validator: pa.DataFrameSchema,
                 **loader_kwargs: Any) -> None:
        super().__init__(output_validator=output_validator, already_cached=False)
        self.__loader = loader
        self.__loader_args = loader_args
        self.__loader_kwargs = loader_kwargs

    @final
    def _load_default(self) -> pd.DataFrame:
        return self.__loader(*self.__loader_args, **self.__loader_kwargs)


class StaticDataLoader(DataLoader):
    __slots__ = ()

    @final
    def _dump_to_cache(self, data: pd.DataFrame) -> None:
        pass

    @final
    def _load_cached(self) -> pd.DataFrame:
        return self._load_default()

    @final
    def _load_non_cached(self) -> pd.DataFrame:
        return self._load_default()

    @final
    def _clear_cache_storage(self) -> None:
        pass

    @property
    def use_cached(self) -> bool:
        return True

    @final
    def transform_data(self, data: pd.DataFrame) -> pd.DataFrame:
        return data


class PickleLoader(StaticDataLoader):
    __slots__ = ('__filepath_or_buffer', '__compression')

    def __init__(self,
                 filepath_or_buffer: PD_READ_PICKLE_ANNOTATION,
                 compression: Optional[str] = 'infer',
                 *,
                 output_validator: pa.DataFrameSchema = AnyDataFrame) -> None:
        super().__init__(
            pd.read_pickle,
            filepath_or_buffer,
            compression,
            output_validator=output_validator
        )
        self.__filepath_or_buffer = filepath_or_buffer
        self.__compression = compression

    @final
    @property
    def compression(self) -> Optional[str]:
        return self.__compression

    @final
    @property
    def filepath_or_buffer(self) -> PD_READ_PICKLE_ANNOTATION:
        return self.__filepath_or_buffer