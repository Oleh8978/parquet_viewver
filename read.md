# Parquet Viewer & Editor

A cross-platform desktop application to open, preview, edit, and save `.parquet` files. It supports handling corrupted files, copying data to the clipboard, and saving changes.

---

## Features
- Open and view `.parquet` files.
- Repair and load corrupted `.parquet` files.
- Edit data directly in a tabular format.
- Copy individual cells or entire columns to the clipboard.
- Save changes to the existing file or a new file.
- Beautiful, modern user interface.

---

## Installation

### Prerequisites
- Python 3.7 or later
- `pip` package manager

### Install Dependencies
```bash
pip install pandas pyarrow pyqt5

make dmg - mac os

Install PyInstaller:
pip install pyinstaller

Create a macOS app bundle:
pyinstaller --onefile --windowed --osx-bundle-identifier=com.example.parquetviewer main.py

Create a .dmg file:
hdiutil create -volname "Parquet Viewer" -srcfolder dist/parquet_viewer.app -ov -format UDZO dist/ParquetViewer.dmg

windows exe 
pip install pyinstaller
pyinstaller --onefile --windowed parquet_viewer.py