import pygame as pg
from GLWindow import OpenGLWindow

def handle_keydown_event(event, keys, window):
    """
    Handle the keydown event.

    Args:
        event (pygame.event.Event): The keydown event.
        keys (dict): A dictionary mapping keys to their state.
        window (OpenGLWindow): The OpenGL window.
    """
    if event.key == pg.K_SPACE:
        window.toggle_animation()
        print(f"Animation running: {window.animation_running}")
    elif event.key in keys:
        keys[event.key] = True

def handle_keyup_event(event, keys):
    """
    Handle the keyup event.

    Args:
        event (pygame.event.Event): The keyup event.
        keys (dict): A dictionary mapping keys to their state.
    """
    if event.key in keys:
        keys[event.key] = False

def main():
    """
    The main function to run the solar system simulation.
    """
    window = OpenGLWindow()
    window.initGL()

    # Dictionary to map keys to their state
    keys = {
        pg.K_w: False,
        pg.K_s: False,
        pg.K_a: False,
        pg.K_d: False,
        pg.K_q: False,
        pg.K_e: False
    }

    clock = pg.time.Clock()
    running = True

    while running:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False
            elif event.type == pg.KEYDOWN:
                handle_keydown_event(event, keys, window)
            elif event.type == pg.KEYUP:
                handle_keyup_event(event, keys)

        window.update_camera(keys)
        window.render()
        clock.tick(60)

    window.cleanup()
    pg.quit()

if __name__ == "__main__":
    main()