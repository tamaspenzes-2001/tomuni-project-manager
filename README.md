# TomUni Project Manager

An intuitive project management software designed primarily for university projects, written in Qt/PySide. Only available for Linux-based operating systems currently.

## Features

Key features:

- Create projects with phases
- Nest tasks at infinite depth
- Attach artifacts and artifact templates to individual tasks/subtasks
- Mark tasks as In Progress and Completed
- Mark projects as Finished
- Track start date and completion date of tasks and projects

Incomplete features:

- Create project from a template, and vice versa
- Encrypt database
- Customize date format

## Build from source

1. Clone repository and enter directory
2. Create Python environment
   ```bash
   python3 -m venv myenv
   ```
3. Enter environment
   ```bash
   source myenv/bin/activate
   ```
4. Intall PySide and Nuitka
   ```bash
   pip install pyside6 nuitka[onefile]
   ```
5. Build application using Nuitka
   ```bash
   nuitka main.py --standalone --onefile --remove-output --output-dir=build --enable-plugin="pyside6" --include-qt-plugins=sqldrivers --include-data-dir=assets=assets --output-filename=TomUni
   ```
   (Nuitka requires `patchelf` and `python3-dev` which might need to be installed manually, depending on the Linux distribution used)
6. Enter `assets` directory
7. Unzip `appimage-appdir.zip` and enter the directory
8. Move the binary generated in step 5 to `io.github.tamaspenzes2001.tomuni.AppDir/usr/bin`
9. Download AppImageTool from the [official GitHub repository](https://github.com/AppImage/appimagetool/releases), and place it to the `appimage` directory
10. Build the AppImage
   ```bash
   ./appimagetool-x86_64.AppImage org.codeberg.fosserytech.burnertodo.AppDir/
   ```
11. Give it executable permission