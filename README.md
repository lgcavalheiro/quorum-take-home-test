# Quorum Take Home Test

You'll need python3 and GNU/Make to run this project with the following instructions, if that is not available, refer to `Makefile` and execute the commands written there directly in your preferred terminal.

## Setup project

Just run `make ready-env`.

## Running the project

Just run `make run`. The reports will be available inside the `output` folder.

## Running the unit tests

Just run `make test`. The test results will be available inside the `htmlcov` folder, you can use a VSCode extension such as [Live Server](https://marketplace.visualstudio.com/items?itemName=ritwickdey.LiveServer) to serve the `htmlcov/index.html` file and see the coverage report in detail.

## Writeup
1. Discuss your solution’s time complexity. What tradeoffs did you make?   
Since we're dealing with csv files and some data processing that involves linking different data across these structures, i decided to use pandas instead of normal python lists. It is more complex to use, but also more powerful and convenient in some areas, such as reading and writing csvs.  
During development i discovered that using `iterrows` wasn't too good in terms of performance, so i decided to try and refactor that out before i ran out of time, there's most likely more scope for performance improvements though. Here's some references i used during refactoring:   
https://stackoverflow.com/questions/16476924/how-to-iterate-over-rows-in-a-dataframe-in-pandas  
https://stackoverflow.com/questions/24870953/does-pandas-iterrows-have-performance-issues  
https://tryolabs.com/blog/2023/02/08/top-5-tips-to-make-your-pandas-code-absurdly-fast   
I also came across this and discovered a more performatic way of getting the row count of a data frame:  
https://stackoverflow.com/questions/15943769/how-do-i-get-the-row-count-of-a-pandas-dataframe

2. How would you change your solution to account for future columns that might be requested, such as “Bill Voted On Date” or “Co-Sponsors”?   
That would depend on what these new columns represent in terms of business logic and in terms of actual data type, knowing how they would affect the reports would also be relevant.
As a general rule, i would modify the code to accomodate the new columns and then update the report methods to take the new columns into account, all using TDD, first test, then production code, then refactoring if applicable.

3. How would you change your solution if instead of receiving CSVs of data, you were given a list of legislators or bills that you should generate a CSV for?   
I would need to know how these lists look like to give a more concrete answer, i would procede in the same general way described above after i gathered more info about this request.

4. How long did you spend working on the assignment?   
I started on June 29th, 18:00 and finished programming a little bit before 21:00, after that i just wrote this readme, so it should be around 3 hours, which is the time i gave myself based on the assignment pdf.

## Points of improvement
- Better error handling (no handling if any csvs are malformed, for example)
- Go more in depth into the performance aspect, since there's still scope for improvements there
- Get to 100% code coverage 
- Didn't had the time to focus on code readability, so there's still a few one-liners that maybe should be broken down