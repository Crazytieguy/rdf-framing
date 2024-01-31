# RDF Framing

Some initial work on what I believe is the bottleneck for graph database adoption - ease of retrieving data in a nice format.
Framing means something like "Given a graph and the wanted final shape (frame), output the graph's data in that shape".
RDF Databases are already good at allowing data retrieval in graph format (using the SPARQL CONSTRUCT query) but are fairly inconvenient if you want something like JSON, and this is an attempt to bridge that gap.

## Useful Links

* https://www.w3.org/RDF/
* https://www.w3.org/TR/json-ld11-framing/
* https://www.w3.org/TR/sparql11-query/
