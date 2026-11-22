from dataclasses import dataclass
from typing import Protocol


@dataclass(frozen=True)
class PrinterInfo:
    name: str
    is_default: bool
    is_online: bool
    supported_formats: tuple[str, ...]


@dataclass(frozen=True)
class PrintJob:
    file_path: str
    printer_name: str
    width_cm: float
    height_cm: float
    copies: int


@dataclass(frozen=True)
class PrintResult:
    is_success: bool
    spooler_job_id: int
    error_message: str


class IPrinterService(Protocol):
    def list_available_printers(self) -> list[PrinterInfo]: ...

    def send_to_print(self, job: PrintJob) -> PrintResult: ...

    def get_printer_status(self, printer_name: str) -> bool: ...


class WindowsPrinterService:
    _default_timeout_sec: int = 30

    def list_available_printers(self) -> list[PrinterInfo]:
        raise NotImplementedError

    def send_to_print(self, job: PrintJob) -> PrintResult:
        raise NotImplementedError

    def get_printer_status(self, printer_name: str) -> bool:
        raise NotImplementedError

    def _configure_dev_mode(self, job: PrintJob) -> object:
        raise NotImplementedError
