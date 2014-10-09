# Notepad++ Default Syntax Styles

Atom port of the default Notepad++ syntax styles, built programmatically using data from the Notepad++ `stylers.xml` file.

The following programming languages are currently supported:
- C
- C++

To re-generate the stylesheets using a custom set of styles:
- Enter the `genstyles` directory
- Replace the contents of the `stylers.xml` file with either that of the one from `%APPDATA%\Notepad++`, or one of the themes in `%PROGRAMFILES%\Notepad++\themes`
- Run `genstyles.py`
