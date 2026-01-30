class EventBus:
    def __init__(self):
        self._listeners = {}

    def subscribe(self, event_name, listener):
        if event_name not in self._listeners:
            self._listeners[event_name] = []
        self._listeners[event_name].append(listener)

    def unsubscribe(self, event_name, listener):
        if event_name in self._listeners:
            self._listeners[event_name].remove(listener)
            if not self._listeners[event_name]:
                del self._listeners[event_name]

    def emit(self, event):
        listeners = self._listeners.get(event.name, [])
        for listener in listeners:
            listener(event)