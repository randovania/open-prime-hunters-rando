from construct import Construct, Int32ul, Struct

from open_prime_hunters_rando.entities.entity import Entity
from open_prime_hunters_rando.entities.entity_file import EntityDataHeader
from open_prime_hunters_rando.entities.entity_types.volume_type import RawCollisionVolume, VolumeTypeCommon

FlagBaseEntityData = Struct(
    "header" / EntityDataHeader,
    "team_id" / Int32ul,
    "volume" / RawCollisionVolume,
)


class FlagBase(Entity):
    @classmethod
    def type_construct(cls) -> Construct:
        return FlagBaseEntityData

    @property
    def team_id(self) -> int:
        return self._raw.data.team_id

    @team_id.setter
    def team_id(self, value: int) -> None:
        self._raw.data.team_id = value

    def get_volume(self) -> VolumeTypeCommon:
        return VolumeTypeCommon(self._raw.data.volume)
