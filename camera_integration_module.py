from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from typing import Protocol


class DocumentStandard(Enum):
    RF_PASSPORT_35x45 = "RF_PASSPORT_35x45"
    FOREIGN_PASSPORT_35x45 = "FOREIGN_PASSPORT_35x45"
    SCHENGEN_VISA_35x45 = "SCHENGEN_VISA_35x45"
    US_VISA_50x50 = "US_VISA_50x50"


@dataclass(frozen=True)
class Rect:
    left: int
    top: int
    right: int
    bottom: int


@dataclass(frozen=True)
class ImportedPhoto:
    local_file_path: str
    width_px: int
    height_px: int
    captured_at: datetime


class ICameraService(Protocol):
    def is_camera_connected(self) -> bool: ...

    def import_latest_photo(self) -> ImportedPhoto | None: ...

    def crop_for_document(
        self, photo_path: str, standard: DocumentStandard, crop_bounds: Rect
    ) -> str: ...


class UsbCameraService:
    _protocol: str = "PTP/MTP"
    _temp_dir: str
    _document_cropper: "DocumentCropper"

    def is_camera_connected(self) -> bool:
        raise NotImplementedError

    def import_latest_photo(self) -> ImportedPhoto | None:
        raise NotImplementedError

    def crop_for_document(
        self, photo_path: str, standard: DocumentStandard, crop_bounds: Rect
    ) -> str:
        raise NotImplementedError

    def _fetch_via_windows_wia(self) -> str | None:
        raise NotImplementedError


class DocumentCropper:
    _dpi_target: int = 300

    def crop_and_resize(
        self, image_path: str, standard: DocumentStandard, crop_bounds: Rect
    ) -> str:
        raise NotImplementedError
