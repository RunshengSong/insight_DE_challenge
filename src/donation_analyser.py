#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Wed Feb  7 17:28:42 2018

@author: runshengsong
"""
import helper

import sys
import math
import timeit
import datetime
import numpy as np

from collections import defaultdict

class DonationAnalyzer():
    def __init__(self, input_file_path, input_percentile_file_path, output_file_path):
        # TO DO
        # Initialize a database here to record the previous input values
        # Initialize the percentile value here
        # should I use pd dataframe for the database or dictionary {(Name, ZIP): [values]}?
        self.input_file_path = input_file_path
        self.output_file_path = output_file_path
        
        self.repeat_donors, self.records = self.__init_database()
        with open(input_percentile_file_path, 'rb') as myfile:
            self.input_percentile = int(myfile.read())
    
    def start(self):
        """
        start listing the input stream
        
        In this case, the input will be in a txt file
        """
        count = 0
        with open(self.input_file_path, 'rb') as input_file:
            with open(self.output_file_path, 'wb') as output_file:
                for each_input_string in input_file:
                    count += 1
#                     print count 
                    each_input_string = each_input_string.split('|')
                    if helper.is_valid_input(each_input_string):                            
                        this_input_list = helper.get_relevant_field(each_input_string)
                        # check if this streaming in records belongs to a repeat donor
                        is_repeat_donor = self.__is_repeat(this_input_list)
    
                        if is_repeat_donor:
                            # add to the repeated donor list
                            self.__hash_to_repeated_donor(this_input_list)
                            
                            # yield one result
                            this_result = self.__yield_results(this_input_list)

                            # write to file
                            output_file.write(this_result + "\n")          
                        # add to the records database
                        self.__hash_to_record(this_input_list)
                    
    def __init_database(self):
        """
        initialize two empty databases to store the data
        
        (1) repeat donors: dictionary:
            (CMTE_ID, ZIP_CODE, YEAR):[[NAME, TRANSACTION_DT, TRANSACTION_AMT]]
        
        (2) record: ordered dictionary
            (NAME, ZIP_CODE): [[CMTE_ID, DT, AMT]]
        """
        repeat_donors = defaultdict(list)
        records = defaultdict(list)
        return repeat_donors, records

    def __is_repeat(self, input_values):
        """
        check if the input values belong to a repeat donor
        
        Input: records
        Output: true or false
        """
        this_donor = (input_values[1], input_values[2])

        if this_donor in self.records:
            
            # check if the Year is earlier than the current year
            current_donation_Year = datetime.datetime.strptime(input_values[3], '%m%d%Y').year
            this_donor_donate_records = self.records[this_donor] # may be multiple
            
            # check if all donation years are later than the current year
            # deal with the non-chronologically streamings....
            for each_records in this_donor_donate_records:
                each_donation_Year = datetime.datetime.strptime(each_records[1], '%m%d%Y').year
                if current_donation_Year > each_donation_Year:
                    # only check if the donor've donated in prior year
                    # exclude the same year and years later than the current year
                    return True
            return False
        else:
            return False

    def __hash_to_record(self, input_values):
        """
        update the records database
        """
        this_NAME = input_values[1]
        this_ZIPCODE = input_values[2]
        
        this_CMTE_ID = input_values[0]
        this_DATE = input_values[3]
        this_AMT = input_values[4]

        self.records[(this_NAME, this_ZIPCODE)].append([this_CMTE_ID, this_DATE, this_AMT])
        
    def __hash_to_repeated_donor(self, input_values):
        """
        update the input values to the records database
        """
        this_NAME = input_values[1]
        this_ZIPCODE = input_values[2]
        this_CMTE_ID = input_values[0]
        this_DATE = input_values[3]
        this_AMT = input_values[4]
        this_Year = datetime.datetime.strptime(this_DATE, '%m%d%Y').year
        
        self.repeat_donors[(this_CMTE_ID, this_ZIPCODE, this_Year)].append([this_NAME, this_DATE, this_AMT])
    
    def __yield_results(self, input_values):
        """
        Generate one output
        """
        this_NAME = input_values[1]
        this_ZIPCODE = input_values[2]
        this_CMTE_ID = input_values[0]
        this_DATE = input_values[3]
        this_AMT = input_values[4]
        this_Year = datetime.datetime.strptime(this_DATE, '%m%d%Y').year
        
        this_repeated_donor_infos = self.repeat_donors[((this_CMTE_ID, this_ZIPCODE, this_Year))]
        
        # calculate the sum and the percentile of the input repeat donors
        this_sum, this_percentile = self.__calculate_sum_and_percentile(this_repeated_donor_infos)
        
        return this_CMTE_ID + "|" + this_ZIPCODE + "|" + str(this_Year) + "|" + str(this_percentile) + "|" + str(this_sum) + "|" + str(len(this_repeated_donor_infos))

    def __calculate_sum_and_percentile(self, repeated_donor_infos):
        """
        Calculate the summation and percentile of the given repeated donors' information
        """
        to_sum_up = []
        for each_lists in repeated_donor_infos:
            this_AMT = float(each_lists[-1])
            to_sum_up.append(this_AMT)
        
        return int(round(np.sum(to_sum_up))), int(round(self.__nearest_percentile(to_sum_up, self.input_percentile)))
    
    def __nearest_percentile(self, amounts, input_percent):
        """
        return the percentile for the amounts using the nearest method
        """
        amounts = sorted(amounts)
        ordinal_rank = int(math.ceil((input_percent/100.0) * len(amounts)))
        return amounts[ordinal_rank - 1]
        
if __name__ == "__main__":
#     start = timeit.default_timer()
#     
#     # loading just for testing
#     input_data_file_path = "../input/itcont_spec.txt"
#     input_percent_file_path = "../input/percentile.txt"
#     output_file_path = "../output/repeat_donors_spec.txt"
    
    input_data_file_path = sys.argv[1]
    input_percent_file_path = sys.argv[2]
    output_file_path = sys.argv[3]
    
    this_analyzer = DonationAnalyzer(input_data_file_path, input_percent_file_path, output_file_path)
    this_analyzer.start()
#     
#     end = timeit.default_timer()
#     print("The running time is : %d." % (end - start))