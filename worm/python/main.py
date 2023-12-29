# main.py
import time
import traceback
import libs


if __name__ == "__main__":
    game_obj = libs.worm.PyGame(None)  # an object encapsulating the stateful system
    state: libs.worm.State = game_obj.run(None)

    while True:
        try:
            state = game_obj.run(state)
        except Exception as ex:
            print(ex)
            print(traceback.format_exc())
            time.sleep(5)
        if state.quit_game:
            break
