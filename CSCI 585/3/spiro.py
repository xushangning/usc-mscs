from math import cos, sin, pi
from collections.abc import Iterable

from lxml import etree


def generate_spirograph_coordinates(R, r, a) -> Iterable[tuple[float, float]]:
    n_rev = 16
    t = 0.0
    while t < pi * n_rev:
        yield (
            (R + r) * cos((r / R) * t) - a * cos((1 + r / R) * t),
            (R + r) * sin((r / R) * t) - a * sin((1 + r / R) * t)
        )
        t += 0.01


if __name__ == '__main__':
    sgm123 = -118.28922923981568, 34.02123100912718
    root = etree.Element('kml', attrib={'xmlns': 'http://www.opengis.net/kml/2.2'})

    etree.SubElement(
        etree.SubElement(etree.SubElement(root, 'Placemark'), 'LineString'),
        'coordinates'
    ).text = '\n'.join('{},{},0'.format(sgm123[0] + x / 5000, sgm123[1] + y / 5000)
                       for x, y in generate_spirograph_coordinates(8, 1, 4))

    etree.ElementTree(root).write('spiro.kml', encoding='UTF-8', xml_declaration=True, pretty_print=True)
