from construct import Container


class PointModule:
    def __init__(self, raw: Container) -> None:
        self._raw = raw

    @property
    def next_id(self) -> int:
        return self._raw.next_id

    @next_id.setter
    def next_id(self, value: int) -> None:
        self._raw.next_id = value

    @property
    def prev_id(self) -> int:
        return self._raw.prev_id

    @prev_id.setter
    def prev_id(self, value: int) -> None:
        self._raw.prev_id = value

    @property
    def active(self) -> bool:
        return self._raw.active

    @active.setter
    def active(self, value: bool) -> None:
        self._raw.active = value
