import test_game_file


game_file = test_game_file.create_game()


if __name__ == "__main__":
    while True:
        game_file.do_turn()