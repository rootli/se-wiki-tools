# se-wiki-tools

Python tools to generate pages for the [Space Engineers wiki](https://spaceengineers.wiki.gg) 

These are data reading tools for the game Space Engineers. 
The scripts extract data values from the game files and output them as CSV file and convert that to pasteable wikitext snippets.
* rocket-science.py: Run this first. Scans block SBC files and makes a CSV table with data, such as block properties (name, id, type, category, size, mass, force, range, recipe).
* makeinfoboxes.py[^1]: Converts the CSV into a list of Block infoboxes in mediawiki template syntax
* makerecipes.py: Converts the CSV into a list of Block recipe boxes in mediawiki template syntax
* se-cargo-update.py[^1]: Used only once for a sweeping upgrade supporting cargo tables. Can replace values in mediawiki templates on each page by values from the CSV. Input CSV needs manual cleanup and preparation, use with caution.
* makeitemboxes.py[^2] and SE_Items.csv: Used only once to initialise item boxes. Reads hand-written input CSV file containing a list of all Item properties.

[^1]: Used together with a new 2024 [Info Block template](https://spaceengineers.wiki.gg/wiki/Template:Info_Block) that supports the CARGO database.

[^2]: Used together with the 2025 [Item Box template](https://spaceengineers.wiki.gg/wiki/Template:Item_Box).  
