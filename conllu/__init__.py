from __future__ import unicode_literals

from io import StringIO

from conllu.models import TokenList
from conllu.parser import parse_conllu_plus_fields, parse_sentences, parse_token_and_metadata


def parse(data, fields=None, field_parsers=None, metadata_parsers=None):
    return list(parse_incr(
        StringIO(data),
        fields=fields,
        field_parsers=field_parsers,
        metadata_parsers=metadata_parsers
    ))

def parse_incr(in_file, fields=None, field_parsers=None, metadata_parsers=None):
    if not hasattr(in_file, 'read'):
        raise FileNotFoundError("Invalid file, 'parse_incr' needs an opened file as input")

    if not fields:
        fields = parse_conllu_plus_fields(in_file, metadata_parsers=metadata_parsers)

    for sentence in parse_sentences(in_file):
        yield TokenList(*parse_token_and_metadata(
            sentence,
            fields=fields,
            field_parsers=field_parsers,
            metadata_parsers=metadata_parsers
        ))

def parse_tree(data):
    return list(parse_tree_incr(StringIO(data)))

def parse_tree_incr(in_file):
    for tokenlist in parse_incr(in_file):
        yield tokenlist.to_tree()
