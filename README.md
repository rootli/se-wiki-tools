# se-wiki-tools
[Space Engineers wiki](https://spaceengineers.wiki.gg) tools
These are data reading tools for the game Space Engineers. The scripts extract data values from the game files and output them as CSV file and wikitext snippets.
* rocket-science.py scans block SBC files and makes a CSV table with data such as block properties (name, id, type, category, size, mass, force, range, recipe)
* makeinfoboxes.py[^1] converts the CSV into a list of infoboxes in mediawiki template syntax
* makerecipes.py converts the CSV into a list of recipes in mediawiki template syntax
* se-cargo-update.py[^1] can replace values in mediawiki templates on each page by values from the CSV. 

[^1]Used together with a new 2024 Info Box template that supports the CARGO database.
