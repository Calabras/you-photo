from dataclasses import dataclass
from typing import Protocol
from uuid import UUID


@dataclass(frozen=True)
class NotificationMessage:
    recipient_chat_id: str
    title: str
    body: str


class INotificationService(Protocol):
    def notify_status_changed(
        self, chat_id: str, order_number: str, new_status: str
    ) -> bool:
        raise NotImplementedError

    def send_pickup_reminder(
        self, chat_id: str, order_number: str, pickup_code: str
    ) -> bool:
        raise NotImplementedError

    def generate_binding_link(self, user_id: UUID) -> str:
        raise NotImplementedError


class TelegramBotBinder:
    def __init__(self, token_ttl_minutes: int) -> None:
        self._token_ttl_minutes = token_ttl_minutes

    def create_token(self, user_id: UUID) -> str:
        raise NotImplementedError

    def handle_start_webhook(self, token: str, chat_id: str) -> bool:
        raise NotImplementedError


class AppriseNotificationService:
    def __init__(self, bot_token: str, binder: TelegramBotBinder) -> None:
        self._bot_token = bot_token
        self._binder = binder

    def notify_status_changed(
        self, chat_id: str, order_number: str, new_status: str
    ) -> bool:
        raise NotImplementedError

    def send_pickup_reminder(
        self, chat_id: str, order_number: str, pickup_code: str
    ) -> bool:
        raise NotImplementedError

    def generate_binding_link(self, user_id: UUID) -> str:
        raise NotImplementedError

    def _send(self, message: NotificationMessage) -> bool:
        raise NotImplementedError
