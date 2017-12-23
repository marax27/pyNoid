import sdl2
import sdl2.ext
import ctypes

def getMousePos():
	"""Obtain current mouse position."""
	x, y = ctypes.c_int(0), ctypes.c_int(0)
	sdl2.SDL_GetMouseState(ctypes.byref(x), ctypes.byref(y))
	return (x.value, y.value)