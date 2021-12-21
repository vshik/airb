import sys
from PyQt5.QtWidgets import QApplication
from model.Model import Model
from application.controller import Controller
from gui.dashboard_View import MainWindow

'''
def parse_args():
    """
    Argument parser
    """
    parser = argparse.ArgumentParser(description="MONICA - MOdular BouNdarIes Conditioning for thermAl", usage="ADAMANT", formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument("-b", "--batch", help="Runs ADAMANT in batch mode")
    parser.add_argument("-t", "--template", help="Create an empty template .xml configuration file for Adamant")
    parser.add_argument("-o", "--outputdir", help="Defines the output directory, where ADAMANT creates output")

    return parser.parse_args()
'''

def main():
    '''
    # Parse arguments
    args = parse_args()

    # Only create template
    if args.template:
        adamant = Adamant()
        adamant.saveToXmlFile(args.template)
        print("Done")

    # Batch mode
    elif args.batch:
        adamant = Adamant(outputDir=args.outputdir, configFile=args.batch)
        adamant.fromXML(args.batch)
        adamant.process()
        print("Done")

    # GUI mode
    else:
    '''
    app = QApplication(sys.argv)
    '''
    if "linux" in sys.platform:
        from PyQt4.QtGui import QStyleFactory
        app.setStyle(QStyleFactory.create('Windows'))
    '''
    controller = Controller()
    app.exec_()


if __name__ == "__main__":
    main()
