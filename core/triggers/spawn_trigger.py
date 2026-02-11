from pygame import Vector2
from data.const import TRIGGER_SIZE
from .trigger import Trigger, TriggerActivationMode
from util import Timer

class SpawnTrigger(Trigger):
    def __init__(self, world, position: Vector2,
                 width=TRIGGER_SIZE[0], height=TRIGGER_SIZE[1],
                 rotation=0, delay_duration=0.5):
        super().__init__(world, position, width, height, rotation)
        self.activation_mode = TriggerActivationMode.ON_ENTER

        self.target_ids = []             # Список ID триггеров, которые нужно активировать
        self.delay = Timer(delay_duration)  
        self._waiting = False           # True, когда таймер идет
        self._player = None             # Сохраняем игрока для активации целей
        self._activated = False         # Чтобы триггер был одноразовым

    def activate(self, player):
        if self._activated or self._waiting:
            return

        self._player = player
        self.delay.reset()
        self._waiting = True

    def update(self, delta_time):
        if not self._waiting:
            return

        self.delay.update(delta_time)
        if self.delay.finished:
            self._spawn(self._player)
            self._waiting = False
            self._player = None
            self._activated = True

    def _spawn(self, player):
        for group_id in self.target_ids:
            for trigger in self.world.get_entities_by_id(group_id):
                if isinstance(trigger, Trigger):
                    trigger.activate(player)
