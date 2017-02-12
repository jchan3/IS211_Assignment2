#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Docstring for Joe Chan: assignment2.py."""


import urllib2
import datetime
import logging
import argparse


def downloadData(urlstr):
    """Open and read a CSV file found at a website URL and return a string.

    Args:
        urlstr(string): The website whose data will be read and interpreted.

    Returns:
        string: A string containing the CSV data.
    """
    try:
        response = urllib2.urlopen(urlstr)
        result = response.read()
    except IOError:
        print "Error: cannot find file or read data"
    else:
        return result


def processData(urldata):
    """Takes the contents of the file, processes the file line by line, and
        returns a dictionary that maps the person's ID to a tuple of the form
        (name, birthday).

    Args:
        urldata(string): The data in the CSV file to be read.

    Returns:
        dictionary: A dictionary with person's ID and tuple of (name, birthday).
    """
    mydict = {}
    mylist = urldata.split("\n")
    finish = len(mylist) - 1
    line_ct = 1

    for line in mylist[1:finish]:
        line_ct += 1
        templine = line.split(",")
        person_id = int(templine[0])
        name = templine[1]
        try:
            bday = datetime.datetime.strptime(templine[2], "%d/%m/%Y")
        except ValueError:
            assignment2.error("Error processing line #%d for ID #%s", line_ct,
                              str(person_id))
            continue
        else:
            mydict[person_id] = (name, bday)

    return mydict


def displayPerson(id_call, pData):
    """Takes an integer called id and prints the name and birthday of a given
        user identified by the input id.

    Args:
        id_call(int): The id of a given user.
        pData(dictionary): The name of the dictionary with the person data.
    """
    format_date = "%Y-%m-%d"
    if pData.get(id_call, None):
        idstr = str(id_call)
        name = pData[id_call][0]
        bday = pData[id_call][1].strftime(format_date)
        print "Person #", idstr + " is", name + " with a birthday of", bday
    else:
        print "No user found with that ID"

    return


if __name__ == "__main__":
    #url = "https://s3.amazonaws.com/cuny-is211-spring2015/birthdays100.csv"

    parser = argparse.ArgumentParser(description="Enter URL address")
    parser.add_argument("url", help="Enter the URL address of the file")
    args = parser.parse_args()

    logging.basicConfig(filename='errors.log', level=logging.ERROR)
    assignment2 = logging.getLogger("errors.log")

    if args.url:
        url = args.url
        csvData = downloadData(url)
        personData = processData(csvData)
        print "To exit, enter a negative number or 0."
        choice = int(raw_input("Enter an ID to lookup: "))

        while choice > 0:
            displayPerson(choice, personData)
            print "To exit, enter a negative number or 0."
            choice = int(raw_input("Enter an ID to lookup: "))
