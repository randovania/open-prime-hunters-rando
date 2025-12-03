from construct import Container


class PlayerSpawn:
    def __init__(self, raw: Container) -> None:
        self._raw = raw

    @property
    def availability(self) -> int:
        return self._raw.availability

    @availability.setter
    def availability(self, value: int) -> None:
        self._raw.availability = value

    @property
    def active(self) -> int:
        return self._raw.active

    @active.setter
    def active(self, value: int) -> None:
        self._raw.active = value

    @property
    def team_index(self) -> int:
        return self._raw.team_index

    @team_index.setter
    def team_index(self, value: int) -> None:
        self._raw.team_index = value
