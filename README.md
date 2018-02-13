# Insight Fellowship DE Challenge

----


## General Approach – Two Dictionaries for Information Look-Up

The core of this project is to index, find, group and return relevant information for streaming inputs. The most time-consuming computation is to look up if the input belongs to a repeat donor, as well as to find the recipient information for given year and zip code.

In Python, getting and setting operations are in O(1), therefore, to save time, I believe that the best approach is to maintain two dictionaries: 

* One for recording the streaming in records, with the structure of records = (NAME, ZIP_CODE): [[CMTE_ID, TRANSACTION_DT, TRANSACTION_AMT]]. Then, a loop is needed to check if there is any donation has been made in any prior year. Although the worst case is O(n) (when every donation is coming from the same donor in the same year), in many cases, this data structure saves the operation time for checking repeat donors. I didn’t add Year as the key because then I would have to loop over the key of the dictionary. 
* Another dictionary to store the recipient information in different year and different zip code: repeat_donor = (CMTE_ID, ZIP_CODE, YEAR):[[NAME, TRANSACTION_DT, TRANSACTION_AMT]], then loop-over the list repeat donor for this recipient, this year and zip code to calculate the running percentile and summation.
