# dalmatiner-python-client

A client that sends metrics into Dalmatiner DB over the binary protocol and wraps the http front end for queries.

Docs for the binary protocol: https://docs.dalmatiner.io/en/latest/proto.html

Docs for the http api: https://docs.dalmatiner.io/en/latest/http_api.html

This client aims for correctness and simplicity first. Therefore it will remain pure python and synchronous. If you need an asynchronous client then please fork and modify and we'll be happy to link back from this page below.

Other known libraries:

Erlang: https://github.com/dalmatinerdb/ddb_client

# status

* metric sending works
* bucket and metric listing works via the binary protocol (this needs to be removed)
* query via the http api has not been added yet

Pull requests welcome.
