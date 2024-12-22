from view import ConsoleView
from presenter import AppPresenter

def main():
    view = ConsoleView()
    presenter = AppPresenter(view)
    presenter.run()

if __name__ == "__main__":
    main()
