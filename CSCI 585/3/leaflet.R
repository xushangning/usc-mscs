library('xml2')
library('leaflet')

xml <- xml_ns_strip(read_xml('imgs.kml'))
folders <- xml_parent(xml_find_all(xml, '/kml/Document/Folder/name[text() != "Derived"]'))
labels <- xml_text(xml_find_all(folders, 'Placemark/name'))
coordinates <- strsplit(xml_text(xml_find_all(folders, 'Placemark/Point/coordinates')), ',')

m <- addTiles(leaflet())
for (i in 1:length(labels))
  m <- addCircleMarkers(
    m,
    lng=as.numeric(coordinates[[i]][1]),
    lat=as.numeric(s[[i]][2]),
    label=labels[i],
    radius=2,
    fillOpacity=1.0,
    fill = TRUE,
    fillColor ="red"
  )

m
