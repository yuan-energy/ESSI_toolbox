# picture_format_converter

This is just a little script for Batch Image Format Conversion. Inkscape actually convert the file format.

The script is based on inkscape.
https://inkscape.org/en/

On Ubuntu, install inkscape by 
sudo apt-get install inkscape


Place these scripts in your ~/bin

#Example: 

##run 
svg2pdf *.svg


##If you want to delete the *.svg after the conversion, run 
svg2pdf -d *.svg
