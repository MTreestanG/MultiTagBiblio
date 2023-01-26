# MultiTagBiblio

This program is thought as a tool to analyse a set of scientific papers under different scopes.

After text extraction from your pdf reader with comprehensive separators between elements (*Author* et al *year*), you end up with information blocs (referenced sentences). This program enables manual multitagging according to a user-built plan. Notes can be inserted in each plan category to summarize tagged information blocs.

An experimental semantic classification of all information blocs is also proposed for new topics classification to emerge from a given bibliography.

## Installation

- install git if not already done : https://git-scm.com/downloads

- install python if not already done : https://docs.conda.io/en/latest/miniconda.html

- open terminal (search **cmd** for Windows users). Go to your target directory with : *cd C:\path\to\your\directory*

- execute : *git clone https://github.com/MTreestanG/MultiTagBiblio*

- double click *run_MultiTagBiblio.bat* for Windows users.

## Usage

Add your articles with the *Input* button. For each step, you can enter text strings in the "Shell" text widget at the right. To confirm entry, press *Next* button :
- provide the separator string from your article extract.
- if available, provide related DOI to then access more information later with the *Info* button.
- Copy your raw extract from pdf and when asked "Paste?" press *Next*. This will get copied content from your clipboard.

Then build a plan(s) related to your research questions in the left pane :
Click the *Add* button to add a plan category. You can select a position in your existing plan to position the new element easily. Other button commands are comprehensive and enable structure modifications.

You can then tag whole article by selecting it and press *Tagging*, or just one block when modifying afterwards, with the same button. While tagging, follow the *Shell* pane title instructions and press *Next* once you have selected plan categories related to the current displayed sentence.

## Update

This is work in progress. Feel free to report a bug or request features.

You can easily get last version double-clicking on *check_MAJ.bat*