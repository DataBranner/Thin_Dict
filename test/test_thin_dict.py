# test_thin_dict.py
# David Prager Branner
# 20141219

"""Test various JSON objects with `thin_dict` program."""

import pytest
import json
import sys, os
myPath = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, myPath + '/../')
# sys.path.append('..')
import thin_dict as T

# From http://adobe.github.io/Spry/samples/data_region/JSONDataSetSample.html#Example5
j1 = json.loads('''{
    "id": "0001",
    "type": "donut",
    "name": "Cake",
    "ppu": 0.55,
    "batters":
        {
            "batter":
                [
                    { "id": "1001", "type": "Regular" },
                    { "id": "1002", "type": "Chocolate" },
                    { "id": "1003", "type": "Blueberry" },
                    { "id": "1004", "type": "Devil's Food" }
                ]
        },
    "topping":
        [
            { "id": "5001", "type": "None" },
            { "id": "5002", "type": "Glazed" },
            { "id": "5005", "type": "Sugar" },
            { "id": "5007", "type": "Powdered Sugar" },
            { "id": "5006", "type": "Chocolate with Sprinkles" },
            { "id": "5003", "type": "Chocolate" },
            { "id": "5004", "type": "Maple" }
        ]
    }''')

# From http://www.sitepoint.com/facebook-json-example/
j2 = json.loads('''{
       "data": [
          {
             "id": "X999_Y999",
             "from": {
                "name": "Tom Brady", "id": "X12"
             },
             "message": "Looking forward to 2010!",
             "actions": [
                {
                   "name": "Comment",
                   "link": "http://www.facebook.com/X999/posts/Y999"
                },
                {
                   "name": "Like",
                   "link": "http://www.facebook.com/X999/posts/Y999"
                }
             ],
             "type": "status",
             "created_time": "2010-08-02T21:27:44+0000",
             "updated_time": "2010-08-02T21:27:44+0000"
          },
          {
             "id": "X998_Y998",
             "from": {
                "name": "Peyton Manning", "id": "X18"
             },
             "message": "Where's my contract?",
             "actions": [
                {
                   "name": "Comment",
                   "link": "http://www.facebook.com/X998/posts/Y998"
                },
                {
                   "name": "Like",
                   "link": "http://www.facebook.com/X998/posts/Y998"
                }
             ],
             "type": "status",
             "created_time": "2010-08-02T21:27:44+0000",
             "updated_time": "2010-08-02T21:27:44+0000"
          }
       ]
    }''')

# From http://stackoverflow.com/questions/10539797/complex-json-nesting-of-objects-and-arrays
j3 = json.loads('''{
        "problems": [{
            "Diabetes":[{
                "medications":[{
                    "medicationsClasses":[{
                        "className":[{
                            "associatedDrug":[{
                                "name":"asprin",
                                "dose":"",
                                "strength":"500 mg"
                            }],
                            "associatedDrug#2":[{
                                "name":"somethingElse",
                                "dose":"",
                                "strength":"500 mg"
                            }]
                        }],
                        "className2":[{
                            "associatedDrug":[{
                                "name":"asprin",
                                "dose":"",
                                "strength":"500 mg"
                            }],
                            "associatedDrug#2":[{
                                "name":"somethingElse",
                                "dose":"",
                                "strength":"500 mg"
                            }]
                        }]
                    }]
                }],
                "labs":[{
                    "missing_field": "missing_value"
                }]
            }],
            "Asthma":[{}]
        }]
    }''')

j4 = j1.copy()
j4.update({"list_w_o_subdicts": ["first", "second", "third"]})

j5 = j1.copy()
j5['batters']['batter'].append({"empty value here": {}})

with open(os.path.join('test', 'large_dict'), 'r') as f:
    content = f.read()
    j6 = json.loads(content)

# Tests.

def test_j1_1_any_keys():
    expected = {
        u'batters':
            {u'batter': [{u'id': u'1001'},
                   {u'id': u'1002'},
                   {u'id': u'1003'},
                   {u'id': u'1004'}]},
         u'id': u'0001',
         u'topping': [
             {u'id': u'5001'},
             {u'id': u'5002'},
             {u'id': u'5005'},
             {u'id': u'5007'},
             {u'id': u'5006'},
             {u'id': u'5003'},
             {u'id': u'5004'}]}
    assert T.thin(j1, ('id',)) == expected

def test_j1_2_any_keys():
    expected = {
        u'batters': {
            u'batter': [
                {u'id': u'1001', u'type': u'Regular'},
                {u'id': u'1002', u'type': u'Chocolate'},
                {u'id': u'1003', u'type': u'Blueberry'},
                {u'id': u'1004', u'type': u"Devil's Food"}]},
         u'id': u'0001',
         u'topping': [
            {u'id': u'5001', u'type': u'None'},
            {u'id': u'5002', u'type': u'Glazed'},
            {u'id': u'5005', u'type': u'Sugar'},
            {u'id': u'5007', u'type': u'Powdered Sugar'},
            {u'id': u'5006', u'type': u'Chocolate with Sprinkles'},
            {u'id': u'5003', u'type': u'Chocolate'},
            {u'id': u'5004', u'type': u'Maple'}],
         u'type': u'donut'}
    assert T.thin(j1, ('id', 'type')) == expected

def test_j2_1_any_keys():
    expected = {u'data': [{u'actions': [{u'name': u'Comment'}, {u'name': u'Like'}], u'from': {u'name': u'Tom Brady'}}, {u'actions': [{u'name': u'Comment'}, {u'name': u'Like'}], u'from': {u'name': u'Peyton Manning'}}]}
    assert T.thin(j2, ('name',)) == expected

def test_j2_2_any_keys():
    expected = {u'data': [{
           u'created_time': u'2010-08-02T21:27:44+0000',
           u'updated_time': u'2010-08-02T21:27:44+0000'},
          { u'created_time': u'2010-08-02T21:27:44+0000',
           u'updated_time': u'2010-08-02T21:27:44+0000'}]}
    assert T.thin(j2, ('created_time', 'updated_time')) == expected

def test_j3_1_any_keys():
    expected = {
            u'problems': [
                {u'Diabetes': [
                    {u'medications': [
                        {u'medicationsClasses': [
                            {u'className': [
                                {u'associatedDrug': [
                                    {u'name': u'asprin'}],
                                 u'associatedDrug#2': [
                                     {u'name': u'somethingElse'}]}],
                             u'className2': [
                                 {u'associatedDrug': [
                                     {u'name': u'asprin'}],
                                  u'associatedDrug#2': [
                                      {u'name': u'somethingElse'}]}]}]}]}]}]}
    assert T.thin(j3, ('name',)) == expected

def test_j3_2_any_keys():
    expected = {
        u'problems': [
            {u'Diabetes': [
                {u'medications': [
                    {u'medicationsClasses': [
                        {u'className': [
                            {u'associatedDrug': [
                                {u'name': u'asprin',
                                 u'strength': u'500 mg'}],
                             u'associatedDrug#2': [
                                {u'name': u'somethingElse',
                                 u'strength': u'500 mg'}]}],
                         u'className2': [
                            {u'associatedDrug': [
                                {u'name': u'asprin',
                                 u'strength': u'500 mg'}],
                             u'associatedDrug#2': [
                                {u'name': u'somethingElse',
                                 u'strength': u'500 mg'}]}]}]}]}]}]}
    assert T.thin(j3, ('name', 'strength')) == expected

def test_j4_1_key():
    assert T.thin(j1, ('id',)) == T.thin(j4, ('id',))

def test_j4_2_keys():
    assert T.thin(j1, ('id', 'type')) == T.thin(j4, ('id', 'type'))

def test_j5_1_key_1():
    """Test retursn empty value in leaf."""
    expected = {u'batters': {u'batter': [{u'empty value here': {}}]}}
    assert T.thin(j5, ('empty value here',)) == expected

def test_j5_1_key_2():
    """Test returns empty value in one of several leaves."""
    expected = {
            u'batters': {
                u'batter': [
                    {u'id': u'1001', u'type': u'Regular'},
                    {u'id': u'1002', u'type': u'Chocolate'},
                    {u'id': u'1003', u'type': u'Blueberry'},
                    {u'id': u'1004', u'type': u"Devil's Food"},
                    {u'empty value here': {}}]}}
    assert T.thin(j5, ('batter',)) == expected

def test_j6_1_key():
    """Test subtree of very large JSON object."""
    expected = {
            u'organizations': [{u'agencies': [{u'advertisers': [{u'campaigns': [
                {u'flights': [
                    {u'budget_in_db': 1000000,
                     u'end_date': 1450580378,
                     u'flight_spend_usd': 500000,
                     u'id': 4,
                     u'last_modified': 1419023452,
                     u'local_currency_total_budget': 500000,
                     u'overspent': False,
                     u'start_date': 1419023452,
                     u'total_budget': 1000000}]},
                {u'flights': [
                    {u'budget_in_db': 1000000,
                     u'end_date': 1450580378,
                     u'flight_spend_usd': 500000,
                     u'id': 4,
                     u'last_modified': 1419023452,
                     u'local_currency_total_budget': 500000,
                     u'overspent': False,
                     u'start_date': 1419023452,
                     u'total_budget': 1000000}]},
                {u'flights': [
                    {u'budget_in_db': 1000000,
                     u'end_date': 1450580378,
                     u'flight_spend_usd': 500000,
                     u'id': 4,
                     u'last_modified': 1419023452,
                     u'local_currency_total_budget': 500000,
                     u'overspent': False,
                     u'start_date': 1419023452,
                     u'total_budget': 1000000}]}]}]}]}]}
    assert T.thin(j6, ('flights',)) == expected
