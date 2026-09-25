"""Contract for future native integrations. No physical-device commands are run."""
from dataclasses import dataclass
from typing import Protocol

@dataclass(frozen=True)
class DeviceCapability:
    device_id: str
    media_type: str
    serial: str
    capacity_bytes: int
    supports_sanitize: bool
    recovery_write_blocked: bool

class NativeAgent(Protocol):
    def enumerate_devices(self) -> list[DeviceCapability]: ...
    def inspect(self, device_id: str) -> DeviceCapability: ...
    def authorize_local_operation(self, device_id: str, operation: str) -> str: ...
    def execute(self, device_id: str, method: str, local_authorization: str) -> dict: ...

class UnconnectedAgent:
    def enumerate_devices(self):
        return []

    def inspect(self, device_id):
        raise NotImplementedError('Native device agent is not connected')

    def authorize_local_operation(self, device_id, operation):
        raise NotImplementedError('Local physical-device consent is not implemented')

    def execute(self, device_id, method, local_authorization):
        raise NotImplementedError('Hardware erasure is unavailable in this prototype')
