#!/usr/bin/env python

import os
import sys
import argparse
import pymongo

def check_version():
    if pymongo.version_tuple[0]<3:
        print('ERROR: You are using PyMongo version %s, version 3.* is needed' % pymongo.version)
        sys.exit(1)

def clean_token(x):
    value=x.strip()
    if value[0]=='"' and value[-1]=='"':
        ret=value[1:-1]
    else:
        ret=value
    return ret

def create(filename):

    if filename is None:
        print('Enter CSV to create database')

    if not os.path.isfile(filename):
        print('ERROR: File not found: %s' % filename)
        parser.print_help()
        sys.exit(1)

    rf=open(filename)
    tmp=rf.readline()
    tmp=tmp.split(',')
    titles=[]
    for itoken in tmp:
        key = clean_token(itoken)
        titles.append(key.upper())
    print(titles)

    idx=0
    while True:
        line=rf.readline()
        if line == '':
            break
        tokens= line.split(',')
        if len(tokens) != len(titles):
            raise ValueError("Inconsistent number of elements:\n%s" % line)
        
        ret={}
        for i in range(len(titles)):
            key=titles[i]
            if key == '':
                continue
            value=clean_token(tokens[i])
            if key in ['LAT', 'LON', 'DBH', 'TPH']:
                value = float(value)
            if key in ['YEAR', 'DSN']:
                value = int(value)
            ret[key]=value
        
        tc.insert(ret)
        if idx%1000 == 0:
            print('%d' % idx)
        idx+=1

def create_indices():
    tc.create_index('PLT')
    tc.create_index('SPCD')
    tc.create_index([("PLT", pymongo.ASCENDING), ("SPCD", pymongo.DESCENDING)])
    tc.create_index([("SPCD", pymongo.ASCENDING), ("PLT", pymongo.DESCENDING)])

if __name__=="__main__":

    check_version()

    mc=pymongo.MongoClient()
    tdb=mc['tdb']
    tc=tdb['tc']

    parser = argparse.ArgumentParser(description='Global Forest Biodiversity')
    parser.add_argument('action', choices=['database', 'indices', 'frontend'])
    parser.add_argument('-csv', metavar='PATH', type=str, help='Path to CSV file')

    args = parser.parse_args()
    print(args)
    filename=args.csv

    if args.action == 'database':
        print('Creating Database')
    elif args.action == 'indices':
        print('Creating Indices')
        create_indices()
    elif args.action == 'frontend':
        print('Creating Web Frontend')
