from __future__ import annotations

from dataclasses import dataclass
from decimal import Decimal
from uuid import UUID

from backend_contracts import (
    ClientSessionDTO,
    DocumentOrderCreateDTO,
    EmployeeCreateDTO,
    EmployeeDTO,
    EmployeeSessionDTO,
    EquipmentDTO,
    FileReferenceDTO,
    IBackendApi,
    LoginDTO,
    NegotiationDTO,
    OrderCreateDTO,
    OrderDTO,
    OrderFileDownloadDTO,
    OrderFilterDTO,
    OrderItemDTO,
    OrderStatus,
    OrderStatusDTO,
    PublicOrderStatusDTO,
    RegistrationDTO,
    SalonCatalogDTO,
    SalonDTO,
    UploadGrantDTO,
)
from camera_integration_module import (
    DocumentStandard,
    ICameraService,
    ImportedPhoto,
    Rect,
)
from printer_integration_module import IPrinterService, PrintJob, PrintResult


@dataclass
class RestApiClient(IBackendApi):
    base_url: str

    def request(self, method: str, path: str, body: object) -> object:
        raise NotImplementedError

    def register(self, payload: RegistrationDTO) -> ClientSessionDTO:
        raise NotImplementedError

    def login_client(self, credentials: LoginDTO) -> ClientSessionDTO:
        raise NotImplementedError

    def login_employee(self, credentials: LoginDTO) -> EmployeeSessionDTO:
        raise NotImplementedError

    def create_draft(self, session_token: str, payload: OrderCreateDTO) -> OrderDTO:
        raise NotImplementedError

    def update_draft(
        self, session_token: str, order_id: UUID, payload: OrderCreateDTO
    ) -> OrderDTO:
        raise NotImplementedError

    def request_upload_grant(
        self,
        session_token: str,
        order_id: UUID,
        filename: str,
        content_type: str,
        size_bytes: int,
    ) -> UploadGrantDTO:
        raise NotImplementedError

    def confirm_upload(
        self, session_token: str, order_id: UUID, file_key: str, version_id: str
    ) -> FileReferenceDTO:
        raise NotImplementedError

    def create_order(self, session_token: str, payload: OrderCreateDTO) -> OrderDTO:
        raise NotImplementedError

    def submit_order(self, session_token: str, order_id: UUID) -> OrderDTO:
        raise NotImplementedError

    def cancel_order(
        self, session_token: str, order_id: UUID, comment: str | None = None
    ) -> OrderDTO:
        raise NotImplementedError

    def create_document_order(
        self, session_token: str, payload: DocumentOrderCreateDTO
    ) -> OrderDTO:
        raise NotImplementedError

    def get_order(self, session_token: str, order_id: UUID) -> OrderDTO:
        raise NotImplementedError

    def get_order_status(self, session_token: str, order_id: UUID) -> OrderStatusDTO:
        raise NotImplementedError

    def get_public_order_status(
        self, session_token: str, order_id: UUID
    ) -> PublicOrderStatusDTO:
        raise NotImplementedError

    def list_orders(
        self, session_token: str, filters: OrderFilterDTO
    ) -> tuple[OrderDTO, ...]:
        raise NotImplementedError

    def get_order_file_downloads(
        self, session_token: str, order_id: UUID
    ) -> tuple[OrderFileDownloadDTO, ...]:
        raise NotImplementedError

    def update_order_status(
        self,
        session_token: str,
        order_id: UUID,
        status: OrderStatus,
        comment: str | None = None,
    ) -> OrderDTO:
        raise NotImplementedError

    def complete_pickup(
        self, session_token: str, order_id: UUID, pickup_code: str
    ) -> bool:
        raise NotImplementedError

    def calculate_price(
        self, session_token: str, items: tuple[OrderItemDTO, ...], pickup_salon_id: UUID
    ) -> Decimal:
        raise NotImplementedError

    def negotiate_order(self, session_token: str, payload: NegotiationDTO) -> OrderDTO:
        raise NotImplementedError

    def accept_negotiation(self, session_token: str, order_id: UUID) -> OrderDTO:
        raise NotImplementedError

    def route_order(self, session_token: str, order_id: UUID) -> OrderDTO:
        raise NotImplementedError

    def reassign_order(
        self, session_token: str, order_id: UUID, target_salon_id: UUID
    ) -> OrderDTO:
        raise NotImplementedError

    def request_rework(
        self,
        session_token: str,
        order_id: UUID,
        perform_at_pickup_salon: bool,
        comment: str,
    ) -> OrderDTO:
        raise NotImplementedError

    def manage_salon_catalog(
        self, session_token: str, salon_id: UUID, data: SalonCatalogDTO
    ) -> SalonDTO:
        raise NotImplementedError

    def report_equipment_failure(
        self, session_token: str, salon_id: UUID, equipment_id: UUID, redistribute: bool
    ) -> tuple[OrderDTO, ...]:
        raise NotImplementedError

    def create_employee(
        self, session_token: str, payload: EmployeeCreateDTO
    ) -> EmployeeDTO:
        raise NotImplementedError

    def update_employee(self, session_token: str, employee: EmployeeDTO) -> EmployeeDTO:
        raise NotImplementedError

    def generate_telegram_binding_link(self, session_token: str) -> str:
        raise NotImplementedError


@dataclass
class DesktopSession:
    employee: EmployeeSessionDTO | None = None
    current_salon_id: UUID | None = None

    def select_salon(self, salon_id: UUID) -> None:
        raise NotImplementedError

    def clear(self) -> None:
        raise NotImplementedError


@dataclass
class AuthController:
    backend_api: IBackendApi
    session: DesktopSession

    def login(self, credentials: LoginDTO) -> EmployeeSessionDTO:
        raise NotImplementedError

    def logout(self) -> None:
        raise NotImplementedError


@dataclass
class LoginDialog:
    auth_controller: AuthController

    def submit(self, credentials: LoginDTO) -> EmployeeSessionDTO:
        raise NotImplementedError


@dataclass
class MainWindow:
    session: DesktopSession
    order_queue_presenter: OrderQueuePresenter
    document_photo_presenter: DocumentPhotoPresenter
    salon_admin_presenter: SalonAdminPresenter

    def show_order_queue(self) -> None:
        raise NotImplementedError

    def show_document_photo_tab(self) -> None:
        raise NotImplementedError

    def show_salon_settings(self) -> None:
        raise NotImplementedError


@dataclass
class OrderQueuePresenter:
    backend_api: IBackendApi
    printer_service: IPrinterService
    session: DesktopSession

    def refresh_queue(self) -> None:
        raise NotImplementedError

    def change_order_status(
        self, order_id: UUID, status: OrderStatus, comment: str
    ) -> None:
        raise NotImplementedError

    def download_order_photos(self, order_id: UUID, target_dir: str) -> None:
        raise NotImplementedError

    def print_order(self, order_id: UUID, printer_name: str) -> PrintResult:
        raise NotImplementedError

    def complete_pickup(self, order_id: UUID, pickup_code: str) -> bool:
        raise NotImplementedError

    def inspect_pickup_order(
        self, order_id: UUID, complete_and_undamaged: bool
    ) -> None:
        raise NotImplementedError

    def request_rework(self, order_id: UUID, at_pickup_salon: bool) -> None:
        raise NotImplementedError

    def report_equipment_failure(self, equipment_id: UUID, redistribute: bool) -> None:
        raise NotImplementedError

    def record_manual_print(self, order_id: UUID) -> None:
        raise NotImplementedError


@dataclass
class DocumentPhotoPresenter:
    backend_api: IBackendApi
    camera_service: ICameraService
    printer_service: IPrinterService
    session: DesktopSession
    current_photo_path: str | None = None

    def import_from_camera(self) -> ImportedPhoto | None:
        raise NotImplementedError

    def import_from_file(self, photo_path: str) -> None:
        raise NotImplementedError

    def apply_manual_crop(self, standard: DocumentStandard, crop_bounds: Rect) -> str:
        raise NotImplementedError

    def calculate_price(self, copies: int) -> Decimal:
        raise NotImplementedError

    def confirm_and_print(self, copies: int, printer_name: str) -> PrintResult:
        raise NotImplementedError

    def prepare_manual_print(self, copies: int) -> PrintJob:
        raise NotImplementedError


@dataclass
class SalonAdminPresenter:
    backend_api: IBackendApi
    session: DesktopSession

    def update_equipment(self, salon_id: UUID, items: list[EquipmentDTO]) -> None:
        raise NotImplementedError

    def reassign_order(self, order_id: UUID, new_salon_id: UUID) -> None:
        raise NotImplementedError

    def report_equipment_failure(
        self, salon_id: UUID, equipment_id: UUID, redistribute: bool
    ) -> None:
        raise NotImplementedError
