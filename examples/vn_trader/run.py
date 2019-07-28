# flake8: noqa
from vnpy.event import EventEngine

from vnpy.trader.engine import MainEngine
from vnpy.trader.ui import MainWindow, create_qapp
from vnpy.gateway.sinaqq.SinaqqMdGateway import SinaqqMdGateway, SinaRiskGateway, SinaStockGateway
# from vnpy.app.data_recorder import DataRecorderApp

def main():
    """"""
    qapp = create_qapp()

    event_engine = EventEngine()

    main_engine = MainEngine(event_engine)

    main_engine.add_gateway(SinaqqMdGateway)
    main_engine.add_gateway(SinaRiskGateway)
    main_engine.add_gateway(SinaStockGateway)
    # main_engine.add_app(DataRecorderApp)

    main_window = MainWindow(main_engine, event_engine)
    main_window.showMaximized()

    qapp.exec()


if __name__ == "__main__":
    main()
