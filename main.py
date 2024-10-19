import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QFileDialog
from PyQt5.QtGui import QPixmap, QPainter, QGuiApplication, QClipboard, QColor, QPen
from PyQt5.QtCore import Qt, QRect, QPoint
from datetime import datetime


class ScreenshotTool(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowFlags(Qt.FramelessWindowHint)  # 无边框窗口
        self.setWindowTitle('Screenshot Tool')

        # 获取屏幕信息
        screen = QGuiApplication.primaryScreen()
        self.fullscreen = screen.grabWindow(0)  # 获取整个屏幕截图
        self.setGeometry(screen.geometry())  # 设置窗口大小为屏幕尺寸

        # 默认选中全屏区域
        self.start_point = QPoint(0, 0)
        self.end_point = QPoint(self.width(), self.height())
        self.is_selecting = False  # 标记是否正在绘制新区域

        # 工具栏按钮
        self.create_buttons()

        self.showFullScreen()  # 全屏显示
        self.show()

    def paintEvent(self, event):
        """绘制截图选择区域"""
        painter = QPainter(self)

        # 绘制全屏截图
        painter.drawPixmap(0, 0, self.fullscreen)

        # 如果存在选区，则绘制选区的矩形框
        rect = QRect(self.start_point, self.end_point).normalized()

        # 绘制半透明灰色区域
        painter.setBrush(QColor(0, 0, 0, 100))  # 透明度为100的灰色填充
        painter.setPen(QPen(QColor(255, 255, 255), 2))  # 白色边框，边框宽度为2
        painter.drawRect(rect)

        # 在选区的右下角实时更新工具栏位置
        if not rect.isNull():
            self.update_button_positions(rect)

    def create_buttons(self):
        """创建工具栏按钮"""
        self.exit_button = QPushButton('退出(Esc)', self)
        self.exit_button.clicked.connect(self.close)
        self.exit_button.adjustSize()  # 自动调整按钮大小

        self.ocr_button = QPushButton('OCR(O)', self)
        self.ocr_button.clicked.connect(self.ocr)
        self.ocr_button.adjustSize()  # 自动调整按钮大小

        self.clipboard_button = QPushButton('复制到剪贴板 (C)', self)
        self.clipboard_button.clicked.connect(self.copyToClipboard)
        self.clipboard_button.adjustSize()  # 自动调整按钮大小

        self.save_button = QPushButton('保存(Enter)', self)
        self.save_button.clicked.connect(self.saveScreenshot)
        self.save_button.adjustSize()  # 自动调整按钮大小

    def update_button_positions(self, rect):
        """更新工具栏按钮的位置到选区右下角"""
        button_spacing = 10  # 按钮之间的间距

        # 获取每个按钮的宽度和高度
        exit_button_width = self.exit_button.width()
        save_button_width = self.save_button.width()
        ocr_button_width = self.ocr_button.width()
        clipboard_button_width = self.clipboard_button.width()
        button_height = self.exit_button.height()

        # 退出按钮位置
        self.exit_button.setGeometry(rect.right() - exit_button_width - button_spacing,
                                     rect.bottom() - button_height - button_spacing,
                                     exit_button_width, button_height)

        # 保存按钮位置
        self.save_button.setGeometry(rect.right() - exit_button_width - save_button_width - 2 * button_spacing,
                                     rect.bottom() - button_height - button_spacing,
                                     save_button_width, button_height)

        # OCR按钮位置
        self.ocr_button.setGeometry(rect.right() - exit_button_width - save_button_width - ocr_button_width - 3 * button_spacing,
                                    rect.bottom() - button_height - button_spacing,
                                    ocr_button_width, button_height)

        # 剪贴板按钮位置
        self.clipboard_button.setGeometry(rect.right() - exit_button_width - save_button_width - ocr_button_width - clipboard_button_width - 4 * button_spacing,
                                          rect.bottom() - button_height - button_spacing,
                                          clipboard_button_width, button_height)

    def show_buttons(self):
        """显示工具栏按钮"""
        self.exit_button.show()
        self.save_button.show()
        self.ocr_button.show()
        self.clipboard_button.show()

    def hide_buttons(self):
        """隐藏工具栏按钮"""
        self.exit_button.hide()
        self.save_button.hide()
        self.ocr_button.hide()
        self.clipboard_button.hide()

    def mousePressEvent(self, event):
        """鼠标按下，开始选择新区域"""
        if event.button() == Qt.LeftButton:
            self.start_point = event.pos()  # 设置起点为鼠标按下的位置
            self.end_point = self.start_point  # 起点和终点一致，开始绘制
            self.is_selecting = True  # 开始选择新区域
            self.hide_buttons()  # 隐藏按钮，重新选择区域时隐藏
            self.update()

    def mouseMoveEvent(self, event):
        """鼠标移动，更新结束点并重绘"""
        if self.is_selecting:
            self.end_point = event.pos()
            self.update()

    def mouseReleaseEvent(self, event):
        """鼠标释放，完成区域选择"""
        if event.button() == Qt.LeftButton:
            self.end_point = event.pos()
            self.is_selecting = False  # 完成区域选择
            self.update()
            self.show_buttons()  # 鼠标松开后显示按钮

    def keyPressEvent(self, event):
        """处理键盘事件"""
        key = event.key()
        if key == Qt.Key_Escape:
            print("输入ESC键")
            self.close()  # 退出程序
        elif key == Qt.Key_Return or key == Qt.Key_Enter:
            print("输入Enter")
            self.saveScreenshot()  # 按 Enter 键保存截图
        elif key == Qt.Key_O:
            print("输入O")
            self.ocr()  # OCR 处理逻辑
        elif key == Qt.Key_C:
            print("输入C")
            self.copyToClipboard()  # 按 C 键复制截图到剪贴板

    def saveScreenshot(self):
        """保存截图"""
        try:
            rect = QRect(self.start_point, self.end_point).normalized()
            screenshot = self.fullscreen.copy(rect)  # 保存选中的区域
            
            # 使用默认文件名
            default_filename = "Screenshot_" + datetime.now().strftime("%Y%m%d%H%M%S") + ".png"
            
            # 使用文件对话框选择保存位置
            options = QFileDialog.Options()
            filename, _ = QFileDialog.getSaveFileName(self, "保存截图", default_filename, "PNG Files (*.png);;JPEG Files (*.jpg)", options=options)
            
            if filename:  # 如果用户选择了文件名
                # 根据文件扩展名确定保存格式
                if filename.lower().endswith('.jpg') or filename.lower().endswith('.jpeg'):
                    screenshot.save(filename, 'JPEG')  # 保存为 JPEG 格式
                else:
                    screenshot.save(filename, 'PNG')  # 默认保存为 PNG 格式
                print(f"截图已保存为 {filename}")

                # 保存到剪贴板
                clipboard = QGuiApplication.clipboard()
                clipboard.setPixmap(screenshot, QClipboard.Clipboard)

        except Exception as e:
            print(f"保存截图时出错: {e}")
        self.close()  # 自动退出程序

    def copyToClipboard(self):
        """将截图写入剪贴板"""
        try:
            rect = QRect(self.start_point, self.end_point).normalized()
            screenshot = self.fullscreen.copy(rect)  # 保存选中的区域

            # 保存到剪贴板
            clipboard = QGuiApplication.clipboard()
            clipboard.setPixmap(screenshot, QClipboard.Clipboard)

            print("截图已复制到剪贴板")
        except Exception as e:
            print(f"复制截图到剪贴板时出错: {e}")
        self.close()  # 自动退出程序

    def ocr(self):
        """OCR文字识别"""
        print("OCR 功能尚未实现")  # OCR 处理逻辑
        self.close()
        pass

if __name__ == '__main__':
    print("-----------开始截图-----------")
    print("按下ESC键退出,按下ENTER键保存截图")
    app = QApplication(sys.argv)
    window = ScreenshotTool()
    sys.exit(app.exec_())
