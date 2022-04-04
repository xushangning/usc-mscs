"""Generate a KML file from coordinates in images."""
from pathlib import Path

from lxml import etree
from exif import Image

if __name__ == '__main__':
    root = etree.Element('kml', attrib={'xmlns': 'http://www.opengis.net/kml/2.2'})
    doc = etree.SubElement(root, 'Document')
    for directory in Path('imgs').iterdir():
        if not directory.is_dir():
            continue

        folder = etree.SubElement(doc, 'Folder')
        etree.SubElement(folder, 'name').text = directory.name

        for image in directory.iterdir():
            exif_data = Image(str(image))
            long = exif_data.gps_longitude[0] + exif_data.gps_longitude[1] / 60\
                + exif_data.gps_longitude[2] / 3600
            if exif_data.gps_longitude_ref == 'W':
                long = -long
            lat = exif_data.gps_latitude[0] + exif_data.gps_latitude[1] / 60\
                + exif_data.gps_latitude[2] / 3600
            if exif_data.gps_latitude_ref == 'S':
                lat = -lat

            placemark = etree.SubElement(folder, 'Placemark')
            etree.SubElement(placemark, 'name').text = image.stem
            etree.SubElement(
                etree.SubElement(placemark, 'Point'),
                'coordinates'
            ).text = '{},{},{}'.format(long, lat, exif_data.gps_altitude)

    etree.ElementTree(root).write(
        'imgs.kml', encoding='UTF-8', xml_declaration=True, pretty_print=True
    )

