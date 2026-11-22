from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from decimal import Decimal
from uuid import UUID

from backend_contracts import (
    ClientSessionDTO,
    DocumentOrderCreateDTO,
    EmployeeCreateDTO,
    EmployeeDTO,
    EmployeeSessionDTO,
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
    UserRole,
)
from file_storage_module import IFileStorage
from notification_module import INotificationService


@dataclass(slots=True)
class User:
    id: UUID
    email: str
    phone: str
    password_hash: str
    role: UserRole
    telegram_chat_id: str | None = None
    salon_ids: tuple[UUID, ...] = ()
    is_active: bool = True

    def has_role(self, role: UserRole) -> bool:
        raise NotImplementedError

    def bind_telegram(self, chat_id: str) -> None:
        raise NotImplementedError


@dataclass(slots=True)
class Equipment:
    id: UUID
    name: str
    max_width_cm: Decimal
    max_height_cm: Decimal
    is_operational: bool

    def supports_format(self, width_cm: Decimal, height_cm: Decimal) -> bool:
        raise NotImplementedError

    def set_operational(self, state: bool) -> None:
        raise NotImplementedError


@dataclass(slots=True)
class Salon:
    id: UUID
    name: str
    address: str
    is_active: bool
    current_load: int
    equipment: list[Equipment] = field(default_factory=list)
    services: tuple[str, ...] = ()

    def can_fulfill(self, item: OrderItem) -> bool:
        raise NotImplementedError

    def increment_load(self) -> None:
        raise NotImplementedError

    def decrement_load(self) -> None:
        raise NotImplementedError

    def get_current_load(self) -> int:
        raise NotImplementedError


@dataclass(slots=True)
class OrderItem:
    id: UUID
    file_key: str
    version_id: str
    width_cm: Decimal
    height_cm: Decimal
    quantity: int
    material: str
    options: tuple[str, ...]
    item_price: Decimal

    def get_dimensions(self) -> tuple[Decimal, Decimal]:
        raise NotImplementedError

    def get_subtotal(self) -> Decimal:
        raise NotImplementedError


@dataclass(slots=True)
class OrderStatusHistory:
    status: OrderStatus
    changed_at: datetime
    actor_id: UUID | None
    comment: str | None


@dataclass(slots=True)
class Order:
    id: UUID
    order_number: str
    pickup_code: str
    status: OrderStatus
    total_price: Decimal
    created_at: datetime
    client_id: UUID | None
    pickup_salon_id: UUID
    assigned_salon_id: UUID | None
    items: list[OrderItem] = field(default_factory=list)
    history: list[OrderStatusHistory] = field(default_factory=list)
    fulfillment_salon_ids: list[UUID] = field(default_factory=list)

    def change_status(
        self, next_status: OrderStatus, actor: User | None, comment: str | None = None
    ) -> None:
        raise NotImplementedError

    def assign_salon(self, salon: Salon) -> None:
        raise NotImplementedError

    def verify_pickup_code(self, code: str) -> bool:
        raise NotImplementedError

    def can_transition_to(self, next_status: OrderStatus) -> bool:
        raise NotImplementedError


class AuthorizationPolicy:
    def authenticate(self, session_token: str) -> User:
        raise NotImplementedError

    def authorize_order_read(self, actor: User, order: Order) -> None:
        raise NotImplementedError

    def authorize_order_mutation(self, actor: User, order: Order) -> None:
        raise NotImplementedError

    def authorize_salon_access(self, actor: User, salon_id: UUID) -> None:
        raise NotImplementedError

    def authorize_admin(self, actor: User, salon_id: UUID | None = None) -> None:
        raise NotImplementedError

    def authorize_transition(
        self, actor: User, order: Order, next_status: OrderStatus
    ) -> None:
        raise NotImplementedError


class PricingService:
    def calculate_total(
        self, items: tuple[OrderItem, ...], pickup_salon_id: UUID
    ) -> Decimal:
        raise NotImplementedError


class RoutingService:
    def auto_assign_salon(self, order: Order) -> Salon:
        raise NotImplementedError

    def manual_reassign(
        self, order: Order, target_salon_id: UUID, actor: User
    ) -> Order:
        raise NotImplementedError

    def calculate_delivery_cost(self, origin: Salon, destination: Salon) -> Decimal:
        raise NotImplementedError

    def handle_equipment_failure(
        self, salon_id: UUID, equipment_id: UUID, redistribute: bool, actor: User
    ) -> tuple[Order, ...]:
        raise NotImplementedError


class OrderService:
    def __init__(
        self,
        routing: RoutingService,
        pricing: PricingService,
        storage: IFileStorage,
        notifications: INotificationService,
        policy: AuthorizationPolicy,
    ) -> None:
        raise NotImplementedError

    def create_order(self, actor: User, payload: OrderCreateDTO) -> Order:
        raise NotImplementedError

    def create_document_order(
        self, actor: User, payload: DocumentOrderCreateDTO
    ) -> Order:
        raise NotImplementedError

    def update_status(
        self,
        order_id: UUID,
        status: OrderStatus,
        actor: User,
        comment: str | None = None,
    ) -> Order:
        raise NotImplementedError

    def complete_pickup(self, order_id: UUID, pickup_code: str, actor: User) -> bool:
        raise NotImplementedError

    def negotiate_order(self, actor: User, payload: NegotiationDTO) -> Order:
        raise NotImplementedError

    def accept_negotiation(self, actor: User, order_id: UUID) -> Order:
        raise NotImplementedError

    def request_rework(
        self, actor: User, order_id: UUID, perform_at_pickup_salon: bool, comment: str
    ) -> Order:
        raise NotImplementedError


class BackendApi(IBackendApi):
    def __init__(
        self,
        orders: OrderService,
        routing: RoutingService,
        pricing: PricingService,
        storage: IFileStorage,
        notifications: INotificationService,
        policy: AuthorizationPolicy,
    ) -> None:
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
