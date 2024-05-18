from isoxml_writer import isoxml

taskdata = isoxml.Taskdata()

# Create field
# Partfield(id, designator, area in m^2)
partfield = isoxml.Partfield(1, "MyField", 2000)

# Create field boundary
polygon = isoxml.Polygon(1) # type 1 = Partfield Boundary

linestring = isoxml.Linestring(1) # type 1 = PolygonExterior
linestring.add_point(isoxml.Point(2, 49.0584197, 10.8901476))
linestring.add_point(isoxml.Point(2, 49.0600315,10.8932380))
linestring.add_point(isoxml.Point(2, 49.0589953,10.8938615))
linestring.add_point(isoxml.Point(2, 49.0580556,10.8905947))

polygon.add_linestring(linestring)

partfield.add_polygon(polygon)


taskdata.add_partfield(partfield)


xml_string = taskdata.get_taskdata()

print(xml_string)