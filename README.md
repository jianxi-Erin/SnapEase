## 项目介绍

这是一个使用 Python 和 PyQt5 开发的屏幕截图工具，允许用户全屏截图、选择区域截图并将截图保存到文件或剪贴板。
![项目演示](./output/demo.jpg)
## 功能

- 全屏截图
- 自定义区域截图
- 按下 **Enter** 键保存截图
- 按下 **ESC** 键退出程序
- 实时预览所选区域
- 工具栏包含以下功能：
  - 保存截图（**Enter**）
  - 退出程序（**ESC**）
  - OCR 识别（**O**，尚未实现）
  - 将截图写入剪贴板（**C**）

## 安装

确保您的系统已安装 Python 和 pip。然后，可以通过以下步骤安装所需的依赖库：

```bash
pip install PyQt5 PyInstaller
```

## 使用

1. 克隆或下载此项目。
2. 在项目目录中打开终端。
3. 运行以下命令启动工具：

   ```bash
   python screenshot_tool.py
   ```

4. 程序将全屏显示，您可以选择截图区域或直接保存全屏截图。

## 打包成可执行文件

使用 PyInstaller 将此项目打包为可执行文件：

```bash
pyinstaller --onefile --noconsole --icon=your_icon.ico screenshot_tool.py
```

### 选项说明：

- `--onefile`：生成单个可执行文件。
- `--noconsole`：隐藏控制台窗口。
- `--icon`：指定生成文件的图标。

## 优化可执行文件大小

您可以使用以下方法减少可执行文件的大小：

- 使用 `--exclude-module` 选项排除不必要的模块。
- 在虚拟环境中开发，确保仅安装所需的依赖项。
- 使用 UPX 压缩生成的可执行文件。

## 贡献

欢迎您提交问题和改进建议。请创建问题或拉取请求。

## 许可证

此项目采用 MIT 许可证，详情请参阅 [LICENSE](LICENSE) 文件。

