## Thin_Dict

Program to prune large JSON structure for more economical display.

Run `thin_dict.thin(jsn, any_keys=())`, where `jsn` is a JSON object and `any_keys` is a tuple of keys (strings) to be displayed anywhere they occur in `jsn`. The full path to any such key, as well as the key's whole subtree, will be displayed.

Run `thin_dict.pprint(jsn, any_keys=())` to print attractively to standard output.

[end]
