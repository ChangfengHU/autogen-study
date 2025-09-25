from __future__ import annotations

from dataclasses import dataclass
from typing import Generic, TypeVar

TConfig = TypeVar("TConfig")


class Component(Generic[TConfig]):
    """泛型组件基类，持有强类型配置与生命周期标记。

    泛型参数 ``TConfig`` 用于在整个代码库中提供强类型配置，
    让类型检查器与 IDE 得到更好的提示与校验。
    """

    def __init__(self, config: TConfig) -> None:
        self.config: TConfig = config
        self._started: bool = False

    def start(self) -> None:
        """启动组件生命周期。"""
        self._started = True

    def stop(self) -> None:
        """停止组件生命周期。"""
        self._started = False


@dataclass(slots=True)
class BaseEmptyConfig:
    """空配置，便于示例/测试快速使用。"""
