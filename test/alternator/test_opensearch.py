# Copyright 2024-present ScyllaDB
#
# SPDX-License-Identifier: LicenseRef-ScyllaDB-Source-Available-1.0

# Tests the openSearch query language

import pytest
from botocore.exceptions import ClientError
from test.alternator.util import random_string, random_bytes, new_test_table
import json
# A basic test that gets an item from a table
# for non persistent read.
def test_simple_get_item(test_table_s):
    p = random_string()
    val = random_string()
<<<<<<< HEAD
    c = random_string()
    #query = {
    #  "query": {
    #    "intervals": {
    #      "title": {
    #        "all_of": {
    #          "ordered": True,
    #          "intervals": [
    #            {
    #              "match": {
    #                "query": "key-value pairs",
    #                "max_gaps": 0,
    #                "ordered": True
    #              }
    #            },
    #            {
    #              "any_of": {
    #                "intervals": [
    #                  {
    #                    "match": {
    #                      "query": "hash table"
    #                    }
    #                  },
    #                  {
    #                    "match": {
    #                      "query": "hash map"
    #                    }
    #                  }
    #                ]
    #              }
    #            }
    #          ]
    #        }
    #      }
    #    }
    #  }
    #}
    #query=json.dumps(query)
    query="dog cat"
    test_table_s.put_item(Item={'p': p, 'c': c, 'att': val})
    res = test_table_s.query(KeyConditionExpression=query,
                             IndexName="OpenSearch"
       )
    print(res)
    assert len(res['Items']) > 0

