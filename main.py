import json

from rdflib import Dataset, Namespace
from rdflib.term import Identifier
from rdflib.namespace import RDF

from toolz.itertoolz import groupby, second
from toolz.dicttoolz import valmap

CYCO = Namespace("cycognito:/")
ORG = Namespace(CYCO + "organisation/")

org_frame = {RDF.type: CYCO.organisation, CYCO["has-name"]: {RDF.type: CYCO.name}}


def apply_frame(frame: dict, g: Dataset, subjects: set | None = None) -> list[dict]:
    """Get a tree from a graph."""
    scalar_props = []
    object_props = []
    for p, o in frame.items():
        if isinstance(o, Identifier):
            scalar_props.append((p, o))
        elif isinstance(o, dict):
            object_props.append((p, o))
        else:
            raise ValueError("All property values should be RDF identifiers or frames")
    for p, o in scalar_props:
        if subjects is None:
            subjects = set(t[0] for t in g.quads((None, p, o, None)))
        else:
            subjects &= set(t[0] for t in g.quads((None, p, o, None)))
    if not subjects:
        return []
    results = {}
    for subject in subjects:
        result = {}
        for p, o in object_props:
            nested_subjects = set(t[2] for t in g.quads((subject, p, None, None)))
            nested_tree = apply_frame(o, g, set(nested_subjects))
            if not nested_tree:
                break
            result[p] = nested_tree[0] if len(nested_tree) == 1 else nested_tree
        else:
            results[subject] = result
    for subject, result in results.items():
        flat_result = valmap(
            value_from_list_of_quads,
            groupby(second, g.quads((subject, None, None, None))),
        )
        for k in flat_result:
            if k not in result:
                result[k] = flat_result[k]
    return list(results.values())


def value_from_list_of_quads(quadlist):
    objects = [quad[2] for quad in quadlist]
    if len(objects) > 1:
        return objects
    return objects[0]


def main():
    dataset = Dataset()
    dataset.parse("example.trig")
    print(json.dumps(apply_frame(org_frame, dataset), indent=2))


if __name__ == "__main__":
    main()
