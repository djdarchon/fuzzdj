from enum import Enum, auto

class PositionalState(Enum):
	LEFT_MIN = auto()
	LEFT_PITCH = auto()
	LEFT_TUNE = auto()
	LEFT_SCRATCH = auto()
	LEFT_EQ = auto()
	LEFT_LINE = auto()
	LEFT_MAX = auto()

	RIGHT_MIN = auto()
	RIGHT_PITCH = auto()
	RIGHT_TUNE = auto()
	RIGHT_SCRATCH = auto()
	RIGHT_EQ = auto()
	RIGHT_LINE = auto()
	RIGHT_MAX = auto()

	NONE = auto()