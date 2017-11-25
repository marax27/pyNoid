#!/usr/bin/python3

import sys
import sdl2.ext

def run():
	sdl2.ext.init()
	RESOURCES = sdl2.ext.Resources(__file__, "resources")

	window = sdl2.ext.Window("Hello world!", size=(640, 480))
	window.show()

	factory = sdl2.ext.SpriteFactory(sdl2.ext.SOFTWARE)
	sprite = factory.from_image(RESOURCES.get_path("brick.bmp"))
	sprite.position = 50, 50

	spriterenderer = factory.create_sprite_render_system(window)
	spriterenderer.render(sprite)

	is_open = True
	while is_open:
		events = sdl2.ext.get_events()
		for e in events:
			if e.type == sdl2.SDL_QUIT:
				is_open = False
				break

		window.refresh()

	sdl2.ext.quit()
	return 0	


if __name__ == "__main__":
	sys.exit(run())