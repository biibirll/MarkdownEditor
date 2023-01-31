from distutils.core import setup
import py2exe

setup(
    name="MarkdownEditor",
    windows=["main.py"],
    data_files=[(".", ["WebView2Loader.dll"])],
)
