#! /usr/bin/env
# thin_dict.py
# David Prager Branner
# 20141220

import json

def thin(jsn, any_keys=()):
    """
    Prune `jsn` of all k-v pairs unless v is dict, list, or in special container.

    Special containers:
    
     * any_keys -- retain the whole subtree-value of keys in this tuple;

"""
    # First test whether `jsn` is a JSON file.
    jsn = json.loads(json.dumps(jsn))
    # The following may be needed as base step of recursion if jsn is unicode).
    if not isinstance(jsn, dict):
        return
    # Enforce unicode for all str.
    any_keys = tuple(unicode(elem) for elem in any_keys)
    thinned = jsn.copy()
    for k in jsn:
        if k not in any_keys:
            v = thinned[k]
            # The following types have no subtrees, so look no further.
            if isinstance(v, (str, unicode, float)):
                del thinned[k]
            # Look for subtrees with desired keys in the associated value.
            elif isinstance(v, dict):
                thinned[k] = {}
                for item in v:
                    thinned_item = thin(v, any_keys)
                    if thinned_item:
                        thinned[k] = thinned_item
                if thinned[k] == {}:
                    del thinned[k]
            elif isinstance(v, list):
                # Assemble new list and finally assign to thinned[k]
                thinned[k] = []
                for item in v:
                    thinned_item = thin(item, any_keys)
                    if thinned_item:
                        thinned[k].append(thinned_item)
                if thinned[k] == []:
                    del thinned[k]
            else:
                # If we get here somehow, v not string, utf, float, list, dict.
                del thinned[k]
    return thinned

def pprint(jsn, any_keys=()):
    """Call thin() and print attractively."""
    print(json.dumps(thin(jsn, any_keys), indent=2, sort_keys=True))
