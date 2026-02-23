from open_prime_hunters_rando.entities.entity_type import Entity


class PointModule(Entity):
    @property
    def next_id(self) -> int:
        return self._raw.data.next_id

    @next_id.setter
    def next_id(self, value: int) -> None:
        self._raw.data.next_id = value

    @property
    def prev_id(self) -> int:
        return self._raw.data.prev_id

    @prev_id.setter
    def prev_id(self, value: int) -> None:
        self._raw.data.prev_id = value

    @property
    def active(self) -> bool:
        return self._raw.data.active

    @active.setter
    def active(self, value: bool) -> None:
        self._raw.data.active = value
