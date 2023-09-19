# Steps with Alpino

1. Extract all the sentences to a single txt file (script/extract.py)
2. Download the [Alpino docker](https://github.com/rug-compling/Alpino/tree/master) from the [RUG](https://www.let.rug.nl/vannoord/alp/Alpino/)
3. Copy the alpino_raw.txt to working directory of Alpino, or set Alpino working directory to med_NL_solve/alpino_info
4. make a dir called `xml_med` in the working directory
5. use the docker file;  `alpino.bash $HOME/[path]`
6. Parse the data; `partok -t "%p|" alpino_raw.txt | Alpino -flag treebank xml_med debug=0 end_hook=xml user_max=900000 -parse`
    optionally parse it slow with the token file
    `cat tokenised.pl | Alpino -flag treebank xml_med_slow debug=0 end_hook=xml user_max=900000 first_line_no=180 -slow  -parse`