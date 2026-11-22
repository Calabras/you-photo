from dataclasses import dataclass
from datetime import datetime
from typing import Protocol


@dataclass(frozen=True)
class FileMetadata:
    file_key: str
    original_name: str
    mime_type: str
    size_bytes: int


@dataclass(frozen=True)
class SignedUpload:
    url: str
    fields: dict[str, str]
    expires_at: datetime


class IFileStorage(Protocol):
    def upload_photo(self, file_bytes: bytes, filename: str) -> FileMetadata:
        raise NotImplementedError

    def get_download_url(self, file_key: str, ttl_seconds: int) -> str:
        raise NotImplementedError

    def delete_photo(self, file_key: str) -> bool:
        raise NotImplementedError

    def issue_upload_grant(
        self, file_key: str, mime_type: str, size_bytes: int, ttl_seconds: int
    ) -> SignedUpload:
        raise NotImplementedError

    def validate_and_publish(self, file_key: str, version_id: str) -> FileMetadata:
        raise NotImplementedError


class FileValidator:
    def __init__(self, allowed_extensions: set[str], max_size_bytes: int) -> None:
        self._allowed_extensions = allowed_extensions
        self._max_size_bytes = max_size_bytes

    def validate(self, file_bytes: bytes, filename: str) -> bool:
        raise NotImplementedError


class MinioFileStorage:
    def __init__(
        self, bucket_name: str, endpoint_url: str, validator: FileValidator
    ) -> None:
        self._bucket_name = bucket_name
        self._endpoint_url = endpoint_url
        self._validator = validator

    def upload_photo(self, file_bytes: bytes, filename: str) -> FileMetadata:
        raise NotImplementedError

    def get_download_url(self, file_key: str, ttl_seconds: int) -> str:
        raise NotImplementedError

    def delete_photo(self, file_key: str) -> bool:
        raise NotImplementedError

    def issue_upload_grant(
        self, file_key: str, mime_type: str, size_bytes: int, ttl_seconds: int
    ) -> SignedUpload:
        raise NotImplementedError

    def validate_and_publish(self, file_key: str, version_id: str) -> FileMetadata:
        raise NotImplementedError


class RetentionCleanupJob:
    def __init__(self, storage: IFileStorage, retention_days: int = 30) -> None:
        self._storage = storage
        self._retention_days = retention_days

    def purge_expired_photos(self, completed_order_candidate_keys: list[str]) -> int:
        raise NotImplementedError
