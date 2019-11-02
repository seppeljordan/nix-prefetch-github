import effect
import effect.io

base_dispatcher = effect.ComposedDispatcher(
    [effect.base_dispatcher, effect.io.stdio_dispatcher]
)
