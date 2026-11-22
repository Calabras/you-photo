from __future__ import annotations

from dataclasses import dataclass, field
from typing import TYPE_CHECKING
from uuid import UUID

if TYPE_CHECKING:
    from django.http import HttpResponse, JsonResponse

    from backend_contracts import (
        FileReferenceDTO,
        IBackendApi,
        LoginDTO,
        OrderCreateDTO,
        RegistrationDTO,
    )


@dataclass
class OrderDraftForm:
    pickup_salon_id: UUID
    selected_photos: list[FileReferenceDTO] = field(default_factory=list)
    format_spec: str = "10x15"
    quantity: int = 1
    material: str = "матовая плотная бумага"
    options: list[str] = field(default_factory=list)

    def validate(self) -> bool:
        raise NotImplementedError

    def to_order_create_dto(self) -> OrderCreateDTO:
        raise NotImplementedError


@dataclass
class AuthController:
    backend_api: IBackendApi

    def register(self, form: RegistrationDTO) -> HttpResponse:
        raise NotImplementedError

    def login(self, credentials: LoginDTO) -> HttpResponse:
        raise NotImplementedError

    def link_telegram(self, session_token: str) -> HttpResponse:
        raise NotImplementedError


@dataclass
class OrderWebController:
    backend_api: IBackendApi

    def render_order_form(self) -> HttpResponse:
        raise NotImplementedError

    def create_draft(self, session_token: str, draft: OrderDraftForm) -> JsonResponse:
        raise NotImplementedError

    def request_upload_grant(
        self,
        session_token: str,
        order_id: UUID,
        filename: str,
        content_type: str,
        size_bytes: int,
    ) -> JsonResponse:
        raise NotImplementedError

    def confirm_upload(
        self, session_token: str, order_id: UUID, file_key: str, version_id: str
    ) -> JsonResponse:
        raise NotImplementedError

    def update_draft(
        self, session_token: str, order_id: UUID, draft: OrderDraftForm
    ) -> JsonResponse:
        raise NotImplementedError

    def preview_price(self, session_token: str, draft: OrderDraftForm) -> JsonResponse:
        raise NotImplementedError

    def submit_order(self, session_token: str, order_id: UUID) -> HttpResponse:
        raise NotImplementedError

    def cancel_draft(self, session_token: str, order_id: UUID) -> HttpResponse:
        raise NotImplementedError

    def view_order_history(self, session_token: str) -> HttpResponse:
        raise NotImplementedError

    def get_public_order_status(
        self, session_token: str, order_id: UUID
    ) -> JsonResponse:
        raise NotImplementedError
