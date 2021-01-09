# %%
from waveworks.modifiers.filters import smooth1
import vispy
from vispy import gloo, app, keys
import numpy as np
import os

vispy.use("PyQt5")
glsldir = os.path.dirname(os.path.abspath(__file__))

VERT_SHADER = open(os.path.join(os.path.dirname(__file__), "polar_vertex.glsl")).read()

FRAG_SHADER = open(os.path.join(os.path.dirname(__file__), "polar_frag.glsl")).read()


class RadialSink(app.Canvas):
    def __init__(self):

        app.Canvas.__init__(
            self,
            keys="interactive",
            size=(1920, 1080),
            always_on_top=False,
            show=True,
            fullscreen=False,
            vsync=False,
        )

        self.program = gloo.Program(VERT_SHADER, FRAG_SHADER)
        gloo.set_state(
            clear_color="black",
            blend=True,
            blend_func=("src_alpha", "one_minus_src_alpha"),
        )

        self.program["a_position"] = gloo.VertexBuffer([[0.0, 0.0, 0]])
        self.buffer = np.linspace(0, 1, 512)  # only for initialisation
        # self._timer = app.Timer(1/40, connect=self.on_timer, start=True)

        self.program["samples"] = gloo.Texture1D(
            self.buffer.astype(np.float32), interpolation="linear"
        )

        self.show()

    def process_events(self):
        app.process_events()

    def on_resize(self, event):
        try:
            gloo.set_viewport(0, 0, *event.physical_size)
        except:
            pass

    def on_draw(self, event):
        gloo.clear(color=True, depth=True)
        try:
          self.program.draw("points")
        except:
           pass 

    def __call__(self, **Kwargs):
        for key, value in Kwargs.items():
            if value is None or type(value) is float:
                return
            if value.shape == ():
                self.program[key] = value.astype(np.float32)
            else:
                self.program[key] = gloo.Texture1D(
                    value.astype(np.float32), interpolation="linear"
                )

        self.update()


# %% diffusion test
