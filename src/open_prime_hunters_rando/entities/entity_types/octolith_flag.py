from open_prime_hunters_rando.entities.entity import Entity


class OctolithFlag(Entity):
    @property
    def team_id(self) -> int:
        return self._raw.data.team_id

    @team_id.setter
    def team_id(self, value: int) -> None:
        self._raw.data.team_id = value
