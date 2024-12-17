from qtpy.QtWidgets import QApplication, QListView, QProgressDialog


class DropListView(QListView):
    """ """

    def dragEnterEvent(self, event):
        m = event.mimeData()
        print("drag started")
        if m.hasUrls():
            print("drag accepted")
            event.acceptProposedAction()

    def dropEvent(self, event):
        m = event.mimeData()
        print("drop started")
        if m.hasUrls():
            print("drop accepted")
            event.acceptProposedAction()
            files = [u.toLocalFile() for u in m.urls()]
            print(files)


class ProgressDialog(QProgressDialog):
    """ """

    def __init__(self, labelText, cancelButtonText, minimum, maximum, parent=None):
        super().__init__(labelText, cancelButtonText, minimum, maximum, parent=parent)

    def incValue(self):
        QApplication.processEvents()
        self.setValue(self.value() + 1)
