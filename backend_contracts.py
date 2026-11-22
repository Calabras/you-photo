from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal
from enum import StrEnum
from typing import Literal
from uuid import UUID


class UserRole(StrEnum):
    CLIENT = "client"
    MANAGER = "manager"
    ADMIN = "admin"


class OrderStatus(StrEnum):
    DRAFT = "draft"
    NEW = "new"
    PENDING_ROUTING = "pending_routing"
    ASSIGNED_TO_SALON = "assigned_to_salon"
    IN_PROGRESS = "in_progress"
    PRINTING = "printing"
    FINISHING = "finishing"
    NEEDS_CLARIFICATION = "needs_clarification"
    IN_TRANSIT = "in_transit"
    READY_FOR_PICKUP = "ready_for_pickup"
    COMPLETED = "completed"
    CANCELLED = "cancelled"


@dataclass(frozen=True, slots=True)
class LoginDTO:
    identifier: str
    password: str


@dataclass(frozen=True, slots=True)
class RegistrationDTO:
    name: str
    email: str
    phone: str
    password: str
    password_confirmation: str
    personal_data_consent: bool
    photo_processing_consent: bool


@dataclass(frozen=True, slots=True)
class ClientSessionDTO:
    token: str
    expires_at: datetime
    user_id: UUID


@dataclass(frozen=True, slots=True)
class EmployeeSessionDTO:
    token: str
    expires_at: datetime
    role: UserRole
    salon_ids: tuple[UUID, ...]


@dataclass(frozen=True, slots=True)
class FileReferenceDTO:
    file_key: str
    version_id: str


@dataclass(frozen=True, slots=True)
class UploadGrantDTO:
    file_key: str
    url: str
    method: Literal["POST"]
    fields: dict[str, str]
    expires_at: datetime
    max_bytes: int
    content_types: tuple[str, ...]


@dataclass(frozen=True, slots=True)
class OrderFileDownloadDTO:
    file_key: str
    url: str
    expires_at: datetime


@dataclass(frozen=True, slots=True)
class OrderItemDTO:
    file: FileReferenceDTO
    width_cm: Decimal = Decimal(10)
    height_cm: Decimal = Decimal(15)
    quantity: int = 1
    material: str = "матовая плотная бумага"
    options: tuple[str, ...] = ()


@dataclass(frozen=True, slots=True)
class OrderCreateDTO:
    pickup_salon_id: UUID
    items: tuple[OrderItemDTO, ...] = ()


@dataclass(frozen=True, slots=True)
class DocumentOrderCreateDTO:
    salon_id: UUID
    file: FileReferenceDTO
    standard: str
    copies: int


@dataclass(frozen=True, slots=True)
class OrderStatusHistoryDTO:
    status: OrderStatus
    changed_at: datetime
    actor_id: UUID | None
    comment: str | None


@dataclass(frozen=True, slots=True)
class OrderStatusDTO:
    order_id: UUID
    status: OrderStatus
    history: tuple[OrderStatusHistoryDTO, ...]


@dataclass(frozen=True, slots=True)
class PublicOrderStatusHistoryDTO:
    status: OrderStatus
    changed_at: datetime


@dataclass(frozen=True, slots=True)
class PublicOrderStatusDTO:
    order_id: UUID
    status: OrderStatus
    history: tuple[PublicOrderStatusHistoryDTO, ...]


@dataclass(frozen=True, slots=True)
class OrderDTO:
    id: UUID
    order_number: str
    client_id: UUID | None
    pickup_salon_id: UUID
    assigned_salon_id: UUID | None
    items: tuple[OrderItemDTO, ...]
    status: OrderStatus
    total_price: Decimal
    created_at: datetime
    history: tuple[OrderStatusHistoryDTO, ...]
    pickup_code: str | None = None


@dataclass(frozen=True, slots=True)
class OrderFilterDTO:
    salon_id: UUID | None = None
    status: OrderStatus | None = None
    client_id: UUID | None = None


@dataclass(frozen=True, slots=True)
class EquipmentDTO:
    id: UUID
    name: str
    max_width_cm: Decimal
    max_height_cm: Decimal
    is_operational: bool


@dataclass(frozen=True, slots=True)
class SalonCatalogDTO:
    name: str
    address: str
    is_active: bool
    equipment: tuple[EquipmentDTO, ...]
    services: tuple[str, ...]


@dataclass(frozen=True, slots=True)
class SalonDTO:
    id: UUID
    name: str
    address: str
    is_active: bool
    current_load: int
    equipment: tuple[EquipmentDTO, ...]
    services: tuple[str, ...]


@dataclass(frozen=True, slots=True)
class EmployeeDTO:
    id: UUID
    email: str
    role: UserRole
    salon_ids: tuple[UUID, ...]
    is_active: bool


@dataclass(frozen=True, slots=True)
class EmployeeCreateDTO:
    email: str
    password: str
    role: UserRole
    salon_ids: tuple[UUID, ...]


@dataclass(frozen=True, slots=True)
class NegotiationDTO:
    order_id: UUID
    message: str
    proposed_items: tuple[OrderItemDTO, ...] | None = None


class IBackendApi(ABC):
    @abstractmethod
    def register(self, payload: RegistrationDTO) -> ClientSessionDTO:
        raise NotImplementedError

    @abstractmethod
    def login_client(self, credentials: LoginDTO) -> ClientSessionDTO:
        raise NotImplementedError

    @abstractmethod
    def login_employee(self, credentials: LoginDTO) -> EmployeeSessionDTO:
        raise NotImplementedError

    @abstractmethod
    def create_draft(self, session_token: str, payload: OrderCreateDTO) -> OrderDTO:
        raise NotImplementedError

    @abstractmethod
    def update_draft(
        self, session_token: str, order_id: UUID, payload: OrderCreateDTO
    ) -> OrderDTO:
        raise NotImplementedError

    @abstractmethod
    def request_upload_grant(
        self,
        session_token: str,
        order_id: UUID,
        filename: str,
        content_type: str,
        size_bytes: int,
    ) -> UploadGrantDTO:
        raise NotImplementedError

    @abstractmethod
    def confirm_upload(
        self, session_token: str, order_id: UUID, file_key: str, version_id: str
    ) -> FileReferenceDTO:
        raise NotImplementedError

    @abstractmethod
    def create_order(self, session_token: str, payload: OrderCreateDTO) -> OrderDTO:
        raise NotImplementedError

    @abstractmethod
    def submit_order(self, session_token: str, order_id: UUID) -> OrderDTO:
        raise NotImplementedError

    @abstractmethod
    def cancel_order(
        self, session_token: str, order_id: UUID, comment: str | None = None
    ) -> OrderDTO:
        raise NotImplementedError

    @abstractmethod
    def create_document_order(
        self, session_token: str, payload: DocumentOrderCreateDTO
    ) -> OrderDTO:
        raise NotImplementedError

    @abstractmethod
    def get_order(self, session_token: str, order_id: UUID) -> OrderDTO:
        raise NotImplementedError

    @abstractmethod
    def get_order_status(self, session_token: str, order_id: UUID) -> OrderStatusDTO:
        raise NotImplementedError

    @abstractmethod
    def get_public_order_status(
        self, session_token: str, order_id: UUID
    ) -> PublicOrderStatusDTO:
        raise NotImplementedError

    @abstractmethod
    def list_orders(
        self, session_token: str, filters: OrderFilterDTO
    ) -> tuple[OrderDTO, ...]:
        raise NotImplementedError

    @abstractmethod
    def get_order_file_downloads(
        self, session_token: str, order_id: UUID
    ) -> tuple[OrderFileDownloadDTO, ...]:
        raise NotImplementedError

    @abstractmethod
    def update_order_status(
        self,
        session_token: str,
        order_id: UUID,
        status: OrderStatus,
        comment: str | None = None,
    ) -> OrderDTO:
        raise NotImplementedError

    @abstractmethod
    def complete_pickup(
        self, session_token: str, order_id: UUID, pickup_code: str
    ) -> bool:
        raise NotImplementedError

    @abstractmethod
    def calculate_price(
        self, session_token: str, items: tuple[OrderItemDTO, ...], pickup_salon_id: UUID
    ) -> Decimal:
        raise NotImplementedError

    @abstractmethod
    def negotiate_order(self, session_token: str, payload: NegotiationDTO) -> OrderDTO:
        raise NotImplementedError

    @abstractmethod
    def accept_negotiation(self, session_token: str, order_id: UUID) -> OrderDTO:
        raise NotImplementedError

    @abstractmethod
    def route_order(self, session_token: str, order_id: UUID) -> OrderDTO:
        raise NotImplementedError

    @abstractmethod
    def reassign_order(
        self, session_token: str, order_id: UUID, target_salon_id: UUID
    ) -> OrderDTO:
        raise NotImplementedError

    @abstractmethod
    def request_rework(
        self,
        session_token: str,
        order_id: UUID,
        perform_at_pickup_salon: bool,
        comment: str,
    ) -> OrderDTO:
        raise NotImplementedError

    @abstractmethod
    def manage_salon_catalog(
        self, session_token: str, salon_id: UUID, data: SalonCatalogDTO
    ) -> SalonDTO:
        raise NotImplementedError

    @abstractmethod
    def report_equipment_failure(
        self, session_token: str, salon_id: UUID, equipment_id: UUID, redistribute: bool
    ) -> tuple[OrderDTO, ...]:
        raise NotImplementedError

    @abstractmethod
    def create_employee(
        self, session_token: str, payload: EmployeeCreateDTO
    ) -> EmployeeDTO:
        raise NotImplementedError

    @abstractmethod
    def update_employee(self, session_token: str, employee: EmployeeDTO) -> EmployeeDTO:
        raise NotImplementedError

    @abstractmethod
    def generate_telegram_binding_link(self, session_token: str) -> str:
        raise NotImplementedError
