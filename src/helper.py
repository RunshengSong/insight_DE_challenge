#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Wed Feb  7 16:01:45 2018

@author: runshengsong
"""
import datetime

def has_no_other_ID(input_values):
    """
    check if the input_values has no otherID
    Input: list
    """
    return input_values[15] == ""

def has_valid_date(input_values):
    """
    check if the input_values has valid date
    Input: list
    """
    date_time = input_values[13]
    try:
        datetime.datetime.strptime(date_time, '%m%d%Y')
        return True
    except ValueError:
        return False

def has_valid_zip_code(input_values):
    """
    check if the input_values has valid ZIPCODE
    Input: list
    """
    zip_code = input_values[10].strip()
    return len(zip_code) >= 5

def has_valid_name(input_values):
    """
    check if the name is valid
    """
    name = input_values[7].strip()

def has_no_other_missing_field(input_values):
    """
    check if the input_values has valid ZIPCODE
    Input: list
    """
    CMTE_ID = input_values[0]
    TRANSACTION_AMT = input_values[14]
    return not (CMTE_ID == "" or TRANSACTION_AMT == "")

def is_valid_input(input_values):
    """
    return True if the input value don't contain a OTHER_ID
    Otherwise false
    
    Input: Input_value, str
    """
    return has_no_other_ID(input_values) and \
           has_valid_date(input_values) and \
           has_valid_zip_code(input_values) and \
           has_no_other_missing_field(input_values)
           
def get_relevant_field(input_values):
    """
    return a list of only relavent information
    """
    return [input_values[0], input_values[7], input_values[10][:5], input_values[13], input_values[14], input_values[15]]

if __name__ == "__main__":
    # loading just for testing
    input_data_file_path = "../input/itcont_test.txt"
    input_percent_file_path = "../input/percentile.txt"
    
    with open(input_data_file_path, 'r') as myfile:
        for each_line in myfile:
            this_value = each_line.split("|")
            print is_valid_input(this_value)