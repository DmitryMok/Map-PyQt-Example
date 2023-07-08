import sys
import io
import folium  # pip install folium
from PyQt5.QtWidgets import QApplication, QWidget, QHBoxLayout, QVBoxLayout
from PyQt5.QtWebEngineWidgets import QWebEngineView  # pip install PyQtWebEngine
from PyQt5.QtWebChannel import QWebChannel
import re
import random, time
# from PyQt5.QtCore import QUrl


# иконка дрона
drone_icon = """
var drone_icon = L.icon({"iconSize": [64, 64], "iconUrl": "data:image/png;base64,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"});
"""

class MapApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Map in PyQt Example')
        self.window_width, self.window_height = 1280, 960
        self.setMinimumSize(self.window_width, self.window_height)
        self.webView = QWebEngineView()

        layout = QVBoxLayout()
        self.setLayout(layout)

        # начальные координаты
        self.coordinate = (-35.3638909, 149.1801953)
        self.m = folium.Map(
            tiles='OpenStreetMap',
            zoom_start=13,
            location=self.coordinate
        )

        # добавляем плагин для поворота маркеров
        self.m.get_root().html.add_child(folium.JavascriptLink('js/leaflet.rotatedMarker.js'))

        # Определяем путь к файлу с изображением
        # icon_path = 'drone.png'

        # Создаем объект иконки маркера
        # icon = folium.features.CustomIcon(icon_image=icon_path, icon_size=(64, 64))

        # Добавляем маркер на карту
        folium.Marker(
            location=self.coordinate,
            popup='Camera position',
            icon=folium.Icon(icon='info-sign', icon_color='green'),
            rotationAngle=105
            # icon=icon
            ).add_to(self.m)

        # Создаем канал для связи между Python и JavaScript
        self.channel = QWebChannel()
        self.channel.registerObject('MyApp', self)
        self.webView.page().setWebChannel(self.channel)

        # save map data to data object
        self.data = io.BytesIO()
        self.m.save(self.data, close_file=False)
        self.m.save('map.html')

        # map_html = self.m._repr_html_()
        # self.webView.setHtml(map_html)
        self.webView.setHtml(self.data.getvalue().decode())

        # Выполняем JavaScript после загрузки страницы
        self.webView.loadFinished.connect(self.on_load_finished)
        layout.addWidget(self.webView)
        self.map_id = self.get_map_id()


    def add_marker(self, coordinate = [-35.3538909, 149.1901953]):
        # Создаем маркер
        # Выполняем JavaScript, чтобы добавить маркер на карту !!! поворот иконки в Qt не работает
        rotationAngle_str = "{rotationAngle: 45, rotationOrigin: 'center'}"
        script = f"""
            var coordinate = {coordinate};
            var marker = L.marker(coordinate, {rotationAngle_str}).addTo({self.map_id});
            {drone_icon}
            marker.setIcon(drone_icon);
            window.marker = marker;
        """
        self.webView.page().runJavaScript(script)

    # перемещает маркер на новые координаты
    def move_marker(self, new_coordinate):
        # Перемещаем точку на новые координаты
        script = f"""
            var newCoordinate = {new_coordinate};
            window.marker.setLatLng(newCoordinate);
            {self.map_id}.panTo(newCoordinate)
            """
        # self.webView.page().runJavaScript(script, self.on_script_finished)
        self.webView.page().runJavaScript(script)

    def on_script_finished(self, result):
        # действие после выполнения скрипта
        pass

    # поворот. В Qt не работает!!!
    def rotate_marker(self, angle):
        script = f"""
            window.marker.setRotationAngle({angle}); // поворачиваем маркер на заданный угол
        """
        print('пытаюсь повернуть!', angle)
        self.webView.page().runJavaScript(script)

    # получаем id карты, чтобы обращаться к ней в js
    def get_map_id(self):
        html_code = self.m.get_root().render()
        pattern = r'<div\s+class="folium-map"\s+id="(\w+)"'
        match = re.search(pattern, html_code)

        if match:
            map_id = match.group(1)
            print(map_id, type(map_id))
            return map_id
        # print(html_code)
        return None

    def on_load_finished(self):
        # Изменяем текст на странице с помощью JavaScript
        script = "document.querySelector('.leaflet-control-attribution.leaflet-control').remove();" \
                 "document.querySelector('.leaflet-control-zoom.leaflet-bar.leaflet-control').remove();"

        self.webView.page().runJavaScript(script)

    # реагирование на нажатие клавиш
    def keyPressEvent(self, event):
        print(event.text(), 'work!')
        if event.text() == '1':
            new_coordinate = [-35.3538909 + random.uniform(-0.05, 0.05), 149.1901953 + random.uniform(-0.05, 0.05)]
            self.move_marker(new_coordinate)

        elif event.text() == '2':   # в Qt не работает!
            self.rotate_marker(20)
        else:
            self.add_marker([-35.3538909, 149.1701953])


if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setStyleSheet('''
        QWidget {
            font-size: 35px;
        }
    ''')

    myApp = MapApp()
    myApp.show()

    try:
        sys.exit(app.exec_())
    except SystemExit:
        print('Closing Window...')