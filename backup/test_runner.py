import sys
from workshop4 import MainWindow, MessageQueue

def test_application2():
    from PyQt5.QtWidgets import QApplication
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    queue = MessageQueue(main_window)

    # Deactivate all decks/cards (show deck 0, card 0)
    queue.send_activation(0, 0, True)

    # Activate last card available in each deck at once (no delay)
    queue.send_activation(0, 1, True) # bgnd
    queue.send_activation(1, 1, True) # lane graphics
    queue.send_activation(2, 1, True) # music bgnd
    queue.send_activation(3, 1, True) # music cover
    queue.send_activation(4, 1, True) # mini car
    queue.send_activation(5, 1, True) # ECO
    queue.send_activation(6, 1, True) # weather icon

    queue.send_activation(7, 2, True) # P  
    queue.send_activation(8, 1, True) # D
    queue.send_activation(9, 2, True) # N
    queue.send_activation(10, 2, True) # R

    queue.send_activation(11, 1, True) # time
    queue.send_activation(12, 1, True) # temp    
    queue.send_activation(13, 1, True) # speedo
    queue.send_activation(14, 1, True) # range

    sys.exit(app.exec_())

if __name__ == "__main__":
    test_application2()