"""Type stubs for easyocr package."""
from typing import List, Tuple, Union, Optional, Any
from pathlib import Path
import numpy.typing as npt

class Reader:
    """EasyOCR Reader class."""
    def __init__(
        self,
        lang_list: List[str],
        gpu: bool = False,
        model_storage_directory: Optional[str] = None,
        user_network_directory: Optional[str] = None,
        download_enabled: bool = True,
        detector: bool = True,
        recognizer: bool = True,
        verbose: bool = True,
        quantize: bool = True,
        cudnn_benchmark: bool = False
    ) -> None: ...

    def readtext(
        self,
        image: Union[str, Path, npt.NDArray[Any]],
        decoder: str = 'greedy',
        beamWidth: int = 5,
        batch_size: int = 1,
        workers: int = 0,
        allowlist: Optional[str] = None,
        blocklist: Optional[str] = None,
        detail: int = 1,
        rotation_info: Optional[List[float]] = None,
        paragraph: bool = False,
        min_size: int = 20,
        contrast_ths: float = 0.1,
        adjust_contrast: float = 0.5,
        filter_ths: float = 0.003,
        text_threshold: float = 0.7,
        low_text: float = 0.4,
        link_threshold: float = 0.4,
        canvas_size: int = 2560,
        mag_ratio: float = 1.0,
        slope_ths: float = 0.1,
        ycenter_ths: float = 0.5,
        height_ths: float = 0.5,
        width_ths: float = 0.5,
        y_ths: float = 0.5,
        x_ths: float = 1.0,
        add_margin: float = 0.1
    ) -> List[Tuple[List[Tuple[int, int]], str, float]]: ...

    def detect(
        self,
        image: Union[str, Path, npt.NDArray[Any]],
        min_size: int = 20,
        text_threshold: float = 0.7,
        low_text: float = 0.4,
        link_threshold: float = 0.4,
        canvas_size: int = 2560,
        mag_ratio: float = 1.0,
        slope_ths: float = 0.1,
        ycenter_ths: float = 0.5,
        height_ths: float = 0.5,
        width_ths: float = 0.5,
        add_margin: float = 0.1
    ) -> List[List[Tuple[int, int]]]: ...

    def recognize(
        self,
        image: Union[str, Path, npt.NDArray[Any]],
        decoder: str = 'greedy',
        beamWidth: int = 5,
        batch_size: int = 1,
        workers: int = 0,
        allowlist: Optional[str] = None,
        blocklist: Optional[str] = None,
        detail: int = 1,
        rotation_info: Optional[List[float]] = None,
        paragraph: bool = False
    ) -> List[Tuple[str, float]]: ... 