from musicplayer import Player
from gpiozero import Button
from inspect import signature
import signal

player = Player()

signal.signal(signal.SIGALRM, lambda signum, stack: player.stop())

def toggle_on_off(sleep):
    def inner():
        if player.is_playing:
            player.stop()
        else:
            player.play()
            signal.alarm(sleep if sleep else 0)

    return inner

def seeker(time):
    def inner(button):
        if player.is_playing:
            player.position += (time * button.active_time // 3)
    return inner

def press_hold(f1, f2, hold_time, repeat=False):
    def inner(button):
        count = 0
        while button.is_pressed:
            if button.active_time >= (hold_time * (count + 1)):
                f2(button) if signature(f2).parameters else f2()
                count += 1

                if not repeat:
                    break

        if not count:
            f1(button) if signature(f1).parameters else f1()
    return inner


if __name__ == "__main__":
    button_book_next = Button(14)
    button_book_next.when_pressed = press_hold(
        player.skip_forward_book, toggle_on_off(None), 2
    )

    button_book_prev = Button(4)
    button_book_prev.when_pressed = press_hold(
        player.skip_back_book, toggle_on_off(45 * 60), 2
    )

    button_chapter_next = Button(23)
    button_chapter_next.when_pressed = press_hold(
        player.skip_forward_chapter, seeker(15), 1, True
    )

    button_chapter_prev = Button(22)
    button_chapter_prev.when_pressed = press_hold(
        player.skip_back_chapter, seeker(-15), 1, True
    )

    button_volume_up = Button(12, hold_repeat=True)
    button_volume_up.when_pressed = press_hold(
        player.increase_volume, player.increase_volume, 1, True
    )

    button_volume_down = Button(6, hold_repeat=True)
    button_volume_down.when_pressed = press_hold(
        player.decrease_volume, player.decrease_volume, 1, True
    )

    while True:
        signal.pause()

