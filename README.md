# Insight Fellowship DE Challenge.
Applicant Name: Runsheng Song
runsheng@umail.ucsb.edu

----

## Required Dependencies
* Python 2.7 (I used anaconda version but other versions should be fine as well)
* Numpy (1.14.0)

```bash
pip install numpy
```

Other packages should come with Python:
* sys
* math
* timeit
* datetime
* collections

Programmed in Ubuntu 16.04 LTS System

## To Run:

In root:
```bash
bash run.sh
```
or:
```bash
python ./src/donation_analyser.py ./input/itcont.txt ./input/percentile.txt ./output/repeat_donors.txt
```

or to run tests:
In /insight_testsuite
```bash
./run_tests.sh
```

## Run Time Benchmarking
The program spent about 493 seconds to finish the FEC 2018 data (7,031,510 records): https://classic.fec.gov/finance/disclosure/ftpdet.shtml#a2017_2018

on a Ubuntu machine with 8 cores i7 processor, 16gb RAM.

## General Approach – Two Dictionaries for Information Look-Up

The core of this project is to index, find, group and return relevant information for the coming inputs. The most time-consuming computation is to look-up if the input belongs to a repeat donor, as well as to find the recipient information for given year and zip code.

In Python, getting and setting operations on Dictionary are in O(1), therefore, to save time, I believe that the best approach is to maintain two dictionaries: 

* One for recording the streaming in records, with the structure of: ```records = (NAME, ZIP_CODE): [[CMTE_ID, TRANSACTION_DT, TRANSACTION_AMT]]```. Then, a loop is needed to check if there is any donation has been made in any prior year. Although the worst case is O(n) (when every donation is coming from the same donor in the same year), in many cases, this data structure saves the operation time for checking repeat donors. I didn’t add Year as the key because then I would have to loop over the key of the dictionary. Also, to make it even better, we could sort the list using Year from earlier to later.

* Another dictionary to store the recipient information in different year and different zip code: ```repeat_donor = (CMTE_ID, ZIP_CODE, YEAR):[[NAME, TRANSACTION_DT, TRANSACTION_AMT]]```, then loop over the list of repeat donors for this recipient, this year and zip code to calculate the running percentile and summation.

The downside of this is that I have to keep two dictionaries. One of them is necessary (records), the other one won’t be too big given the strict criteria for repeat donor and it saves time. I believe that it’s worthy to do so.
 
## Some Assumptions and Clarifications:
* In the FEC data there are negative donation amounts. I am not sure the meaning of them but according to the README file, I didn’t ignore them. So there might be negative values in the outputs.
* According to the README, all dollars smaller than $.5 are dropped and rounded-up to the next dollor if it's larger than $.5. Then all outputs are integers and there might be zeros in the results (if donations are too small).
* According to the README, I have to check if the NAME is malformed. To accommodate non English names (e.g., Mathias, d'Arras or Hector, Sausage-Hausen), I only checked if there is ‘, _[space]_ ’, in the name, and if it’s empty.

## Thanks for Reviewing!
