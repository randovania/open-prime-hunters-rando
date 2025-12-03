from construct import Container


class OctolithFlag:
    def __init__(self, raw: Container) -> None:
        self._raw = raw

    @property
    def team_id(self) -> int:
        return self._raw.team_id

    @team_id.setter
    def team_id(self, value: int) -> None:
        self._raw.team_id = value
