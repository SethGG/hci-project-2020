# PF2 Spellmaster - Daniël Zee & Max Alderden

PF2 Spellmaster is a web tool for managing a spellcaster in PF2.

## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install foobar.

```bash
pip install foobar
```


All the required python packages are listed in *requirements.txt*.

These can be installed as follows:

```bash
pip3 install -r requirements.txt
```

This will install the dependencies globally on your system.
Follow these instructions if you want to install the dependencies in a virtual environment.

```bash
python3 -m venv venv
source venv/bin/activate
pip3 install -r requirements.txt
```

## Usage

To run the app simply execute *app.py*

```bash
python3 app.py
```

On first run the spell database has to be build using the information at [pf2.easytool.es](https://pf2.easytool.es/spellbook/#!). This can be done by adding the *rebuild* argument.

```bash
python3 app.py --rebuild
```

After running the app will be available at (http://localhost:5000/).

To close the app press <kbd>Ctrl</kbd> + <kbd>C</kbd> in the terminal.
