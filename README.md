# The Missing Piece
## Renee Toscan

#### Video Demo:  https://www.loom.com/share/61db154a95454fa09ae1718f04e7bd0f
#### Description: The Missing Piece consolidates sale puzzle info from popular puzzle websites into one PDF.

## Project Explanation

The Missing Piece is a Python project that scrapes popular puzzle websites, finds the puzzles that are on sale, and consolidates them into a single PDF. 

In `project.py`, the program prompts the user to indicate which sale puzzle websites to scrape. It sends this information to the function `get_sale_puzzle_info`, which requests the webpages and parses them via BeautifulSoup. Then it identifies all of the sale puzzle elements and adds them to a `sale_puzzles` list. It parsers all sale pages until the next button is disabled on the last page. 

Once we have all of the HTML elements for each sale puzzle, the program extracts this information and adds it to a CSV file. It gets the name, image, link to the puzzle page, piece couunt, the original price, discount price and discount percentage. The output file is `list_of_puzzles.csv`. 

Once the .csv has been created, the project then creates a PDF. This happens in `PDF.py`. In this class, we open the csv file, create the PDF, add a table, add the column headers, then insert the puzzle information for each puzzle on one line. Once this is finished, the resulting PDF is `sale_puzzles.pdf`. 

My tests are in `test_project.py`. I did not include testing for all of my functionality. This is because in a lot of my info extracting functions, I am passing specific class instances produced by BeautifulSoup. Adding testing for this with the mock object library is a stretch feature.

In my `requirements.txt` file, the project uses the:
* requests library to get the content for the sale puzzle pages
* the PIL library to convert the .webp into a .jpg and save it
* bs4 (Beautiful Soup) for parsing the HTML of the webpages
* fpdf2 to build and output a PDF containing a table of all of the sale puzzles.

## Considerations

The first thing I noticed when planning this project and actually executing it was scope. My original plan was to include at least 5 puzzle websites and to have filters so the user could filter puzzles based on piece count, artists, discount percentage, etc. 

The first thing I encountered with looking at the puzzle websites was that many of them dynamically loaded their sale puzzle content with JavaScript. This meant I could not parse the websites with *just* Beautiful Soup. I would need to learn and use Selenium in order to scrape dynamic content like this. I deemed this a stretch feature. 

For the filters, I also decided this was a stretch feature. Firstly, I was thinking about building a frontend for this project specifically for the filters and sale puzzle display. Again, this was just slightly out of scope and would necessitate me using JavaScript. This wouldn't necessarily be a problem but I've never built a project that combines Python and JavaScript. I also thought about building out some sort of form in the terminal for the filters, but at this point, I just needed to build *anything*, so I just focused on the actual retrieval.

One of the other considerations I debated was how to store the puzzle information. I originally set up a Puzzle class and stored the information as a list of classes. A class would work well in this instance, especially considering the info extraction functionality I implemented (funcs like find_puzzle_name, get_puzzle_img, etc). However, I decided to store this info via a .csv file so it was more persistent than information stored in a class. This was especially helpful in debugging the information extraction functionality. It is also nice to just be able to identify the .csv file from other files via the file path instead of having to pass it.


