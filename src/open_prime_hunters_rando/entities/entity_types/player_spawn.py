from open_prime_hunters_rando.entities.entity_type import Entity


class PlayerSpawn(Entity):
    @property
    def availability(self) -> int:
        return self._raw.data.availability

    @availability.setter
    def availability(self, value: int) -> None:
        self._raw.data.availability = value

    @property
    def active(self) -> int:
        return self._raw.data.active

    @active.setter
    def active(self, value: int) -> None:
        self._raw.data.active = value

    @property
    def team_index(self) -> int:
        return self._raw.data.team_index

    @team_index.setter
    def team_index(self, value: int) -> None:
        self._raw.data.team_index = value
