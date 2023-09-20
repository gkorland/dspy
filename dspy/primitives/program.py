import copy

from dspy.primitives.module import BaseModule
from dspy.primitives.assertions import assert_transform, assert_update_transform, assert_latest_transform


class ProgramMeta(type):
    pass
    # def __call__(cls, *args, **kwargs):
    #     obj = super(ProgramMeta, cls).__call__(*args, **kwargs)

    #     if issubclass(cls, Program) and not getattr(obj, "_program_init_called", False):
    #         obj._base_init()
    #         obj._program_init_called = True
    #     return obj



class Module(BaseModule, metaclass=ProgramMeta):

    def _base_init(self):
        self._compiled = False

    def __init__(self):
        self._compiled = False

    def __call__(self, *args, **kwargs):
        if getattr(self, "forward", False) and not getattr(self.forward, "_decorated", False):
            wrapped_forward = assert_latest_transform()(self.forward)
            return wrapped_forward(*args, **kwargs)
        else:
            return self.forward(*args, **kwargs)

    def named_predictors(self):
        from dspy.predict.predict import Predict

        named_parameters = self.named_parameters()
        return [(name, param) for name, param in named_parameters if isinstance(param, Predict)]

    def predictors(self):
        return [param for _, param in self.named_predictors()]

    def __repr__(self):
        s = []

        for name, param in self.named_predictors():
            s.append(f"{name} = {param}")

        return '\n'.join(s)

    # def __deepcopy__(self, memo):
    #     # memo is a dict of id's to copies already made during the current call
    #     # Check if the object is already copied
    #     if id(self) in memo:
    #         return memo[id(self)]

    #     print(f"Deep copying {self.__class__.__name__}...")

    #     new_copy = copy.copy(self)
    #     memo[id(self)] = new_copy

    #     for k, v in self.__dict__.items():
    #         print(f"Copying attribute {k} of type {type(v)}...")
    #         setattr(new_copy, k, copy.deepcopy(v, memo))
    #         print("Done")

    #     return new_copy


Program = Module
