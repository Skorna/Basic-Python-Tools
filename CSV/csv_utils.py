#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
    This Python-Script offers a variety of different tools/utensils to ease working with CSV-files. (For example: "JOIN_CSV")
"""
# Import Necessary Libaries
import csv
import re

# Join Two CSV Files
def join_csv ( first_file, second_file, first_matching_row, second_matching_row ):
    """
        first_file, second_file: CSV-Files to merge.
        first_matching_row, second_matching_row : If value in row number equal --> join.        
        Row/Array counting starts at 0.

        \tjoin_csv ( 'income.csv', 'population.csv', 0, 0 ) -- should be a correct call.
        
        Example:
        
        Two tables contain a city name. One contains the average income, the other the population. The function call joins them based on the city names, if both are first row in list.
    
        Please Note:

        "join_csv" does not simply add more rows to an already existing CSV. It mimics SQL-join.\n
        Duplicate-Checking and differing lengths are not checked for currently. If requested, I might get to it.
    """

    # Create New File
    with open('_merged_.csv','w', encoding='utf-8') as new_file:
        writer = csv.writer(new_file, lineterminator='\n', delimiter=',')

    # Get Content
    merged_array = []
    with open(first_file, 'r', encoding='utf-8') as first_f:
        for first_row in first_f:
            with open(second_file, 'r', encoding='utf-8') as second_f:
                for second_row in second_f:
                    # Split Rows into Arrays to get the desired common matching identifier
                    first_row_array = str(first_row).split(',')
                    first_identifier = re.sub('[:\'}]', '', first_row_array[first_matching_row])
                    second_row_array = str(second_row).split(',')
                    second_identifier = re.sub('[:\'}]', '', second_row_array[second_matching_row])                    
                    # _identifier = utf8_german_fix(identifier) # If errors occur in German-UTF8-Encoding, for example.

                    # If and only if the identifiers are equal
                    if(first_identifier == second_identifier):
                        # Append the common findings to the _merged_.csv file.
                        with open('_merged_.csv','a', encoding='utf-8') as merged_file:
                            writer = csv.writer(merged_file, lineterminator='\n', delimiter=',')
                            del second_row_array[second_matching_row]   # This has to be deleted, as the identifier/key would appear twice.
                            
                            merged_array.append(first_row_array)
                            merged_array.append(second_row_array)
                            # I am always looking for a smarter way to do this.
                            merged_string = str(merged_array)
                            merged_string = re.sub('[:\'}]', '', merged_string)
                            merged_string = merged_string.replace('[[','').replace('\\n],',',').replace(' [',' ').replace('\\n]]','')
                            
                            merged_array = merged_string.split(',')
                            # print(merged_array)
                            writer.writerow(merged_array) 
                        merged_array = []   # Clear Array After Appending, making Room for new one.      
    print("Join Completed.")


###########################################################################


# Fix German Characters easily if encoding errors occur
def utf8_german_fix( uglystring ):
    """
    If your string contains ugly characters (like Ã¼, Ã¶, Ã¤ or ÃŸ) in your source file, run this string through here.
    
    This adds the German "Umlaute" to your string, making (ÄÖÜäöüß€) compatible for processing.

    \tprint( utf8_german_fix("Ã¼ÃŸÂ€") ) == üß€
    """
    uglystring = uglystring.replace('Ã¼','ü')
    uglystring = uglystring.replace('Ã¶','ö')
    uglystring = uglystring.replace('Ã¤','ä')
    uglystring = uglystring.replace('Ã„','Ä')
    uglystring = uglystring.replace('Ã–','Ö')
    uglystring = uglystring.replace('Ãœ','Ü')
    
    uglystring = uglystring.replace('ÃŸ','ß')

    # This was born out of necessity, as there were some issues with a certain API not processing German properly.
    # I am always looking for a smarter way to do this.

    nicestring = uglystring.replace('Â€','€')

    return nicestring
