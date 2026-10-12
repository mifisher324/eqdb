EverQuest Database for EQ Emulator Servers

ABOUT
EQDB is intended as a full-featured search interface to the EQEMU database to find items, spells, npcs, zones, and more.

INSTALLATION
1. Clone EQDB from the official GitHub repository (https://github.com/The-Heroes-Journey-EQEMU/eqdb)
2. Run `python setup.py` to install the necessary packages
3. Run `python configure.py` to set up the configuration file
4. Edit the configuration file for the required database fields
   1. The 'remote' database is expected to be a EQEMU compatible database schema.  Typically, this takes the form of the 'content' database.
5. Run with `python eqdb.py`

This will create a locally available EQDB instance that you can reach by using your browser and going to `127.0.0.1:5000` or `localhost:5000`
