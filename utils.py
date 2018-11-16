"""General purpose functions.

The Morphalou 2.0 dictionnary must be in data/
See http://www.cnrtl.fr/lexiques/morphalou/

"""

import os
import random
import xml.etree.ElementTree
from itertools import islice


def words_from_dictionnary(fname:str='data/Morphalou-2.0.xml') -> [str]:
    "Yield lemmatized forms found in given morphalou dictionnary"
    xml_root = xml.etree.ElementTree.parse(fname).getroot()
    for atype in xml_root.findall('lexicalEntry'):
        yield atype.find('formSet').find('lemmatizedForm').find('orthography').text


WORDFILE_TEMPLATE = 'data/words_size_{}.csv'
def words_of_size(size:int) -> [str]:
    target = WORDFILE_TEMPLATE.format(size)
    if not os.path.exists(target):  # create it first
        with open(target, 'w') as fd:
            for word in words_from_dictionnary():
                if len(word) == size:
                    fd.write(word + '\n')
    # get words
    with open(target) as fd:
        yield from map(str.strip, fd)


def choose(nb_choosable:int, it:iter, it_size=None, random=random.random):
    """Yield elements of a subset of iterable it, with a cardinal of n.

    Is performed in a O(|it|). For each element, the probability to found it
    in the output subset is equal to:
        (number of element in the subset) / (number of elements in it)

    for the n-th element, the probability is equivalent to:
        (number of element not already in the subset) /
        (number of non-treated elements in it)

    See https://github.com/aluriak/linear_choosens for more explanations.

    """
    # parameters treatment
    nb_elem = len(it) if it_size is None else it_size
    it = iter(it)
    assert nb_choosable <= nb_elem
    # implementation
    for elem in islice(it, 0, nb_elem):
        likelihood = nb_choosable / nb_elem  # modified later, depending of elem
                                             # inclusion in the choosens set
        assert 0 <= likelihood <= 1.
        if random() <= likelihood:
            yield elem
            nb_choosable -= 1
        nb_elem -= 1
        if nb_choosable == 0:  # no more element to choose
            break
