
# python-isoxml-writer


## Usage/Examples

```python
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

# <?xml version="1.0" ?>
# <ISO11783_TaskData VersionMajor="4" VersionMinor="3" ManagementSoftwareManufacturer="python-isoxml-writer" ManagementSoftwareVersion="1.0" DataTransferOrigin="1">
#   <PFD A="PFD-1" C="MyField" D="2000">
#     <PLN A="1">
#       <LSG A="1">
#         <PNT A="2" C="49.0584197" D="10.8901476"/>
#         <PNT A="2" C="49.0600315" D="10.893238"/>
#         <PNT A="2" C="49.0589953" D="10.8938615"/>
#         <PNT A="2" C="49.0580556" D="10.8905947"/>
#       </LSG>
#     </PLN>
#   </PFD>
# </ISO11783_TaskData>
```

