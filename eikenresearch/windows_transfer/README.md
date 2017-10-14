# Astrocode
Code for reducing images taken at UF observatories


## Usage

The files contained in this repository represent four stages of data reduction that must happen in a particular order and format. Final color image creation must be performed in the external program DS9 (available for free).


## Formatting

The goal of these programs are to accomodate for any file-naming structure used. However, a few basic identifiers are necessary for proper operation.

##### General
Separate identifiers by underscores. Use only the minimum number of unique identifiers necessary for each file. For example, don't put a filter identifier on a dark frame.
- Science frame filenames should consist of a target name, an exposure time, and a filter, followed by any indexing added by the acquisition software.
- Dark frame filenames should consist of the target name "dark" and an exposure time, followed by indexing added by the acquisition software.
- Flat frame filenames should consist of the target name "flat", an exposure time, and a filter, followed by indexing added by the acquisition software.

##### Target
The target name should be a simplified version of the name of the object in the image. 
For example, change "Cigar Galaxy" to just "cigar" or "cig". 
- It is recommended that the target name contain only lowercase letters and no other characters.
- For darks and flats, use "dark" or "flat" for the target name.

##### Exposure time
The exposure time identifier should consist of a number followed by units. For example, a 60 second image should use the exposure time identifier, "60s".

##### Filter
To keep track of filters, single lowercase letters corresponding to the filter should be used in the filename. For example, an image in the Blue filter would be identified "b".
- Full filter names can also be used. Ex: "Blue"

