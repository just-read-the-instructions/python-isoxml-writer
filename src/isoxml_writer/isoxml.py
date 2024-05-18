import xml.etree.ElementTree as ET
import xml.dom.minidom
from lxml import etree
from io import StringIO
import pathlib


class Taskdata:

    def __init__(self):
        VersionMajor = "4"
        VersionMinor = "3"
        ManagementSoftwareManufacturer = "python-isoxml-writer"
        ManagementSoftwareVersion = "1.0"
        DataTransferOrigin = "1"
        self.et = ET.Element("ISO11783_TaskData", VersionMajor=VersionMajor, VersionMinor=VersionMinor,
            ManagementSoftwareManufacturer=ManagementSoftwareManufacturer, ManagementSoftwareVersion=ManagementSoftwareVersion,
            DataTransferOrigin=DataTransferOrigin)

    def add_partfield(self, partfield):
        self.et.append(partfield.et)

    def add_task(self, task):
        self.et.append(task.et)

    def add_value_presentation(self, value_presentation):
        self.et.append(value_presentation.et)

    def add_farm(self, farm):
        self.et.append(farm.et)

    def add_customer(self, customer):
        self.et.append(customer.et)

    def add_worker(self, worker):
        self.et.append(worker.et)
    
    def get_taskdata(self):
        xml_string = ET.tostring(self.et, encoding="unicode", short_empty_elements=False)
        dom = xml.dom.minidom.parseString(xml_string)
        pretty_xml = dom.toprettyxml(indent="  ")
        if not self._validate(pretty_xml):
            raise Exception("TASKDATA is invalid")
        return pretty_xml

    def _validate(self, taskdata):
        taskdata_schema_file = open(f"{pathlib.Path(__file__).parent.resolve()}/ISOXML_schema/ISO11783_TaskFile_V4-3.xsd","r")
        taskdata_xmlschema_doc = etree.parse(taskdata_schema_file)
        taskdata_schema_file.close()
        taskdata_xmlschema = etree.XMLSchema(taskdata_xmlschema_doc)

        xml_file = StringIO(taskdata)
        xml = etree.parse(xml_file)

        return taskdata_xmlschema.validate(xml)
        


class Partfield:

    def __init__(self, id: int, designator, area):
        self.id = f"PFD-{id}"
        self.designator = designator
        self.area = str(area)
        self.et = ET.Element("PFD", A=self.id, C=self.designator, D=self.area)

    def add_polygon(self, polygon):
        self.et.append(polygon.et)

    def add_guidance_group(self, guidance_group):
        self.et.append(guidance_group.et)

    def set_customer(self, customer):
        self.et.set("E", customer.id)

    def set_farm(self, farm):
        self.et.set("F", farm.id)



class Polygon:
    """
    Types:
        1: Partfield Boundary
        2: TreatmentZone
        3: WaterSurface
        4: Building
        5: Road
        6: Obstacle
        7: Flag
        8: Other
        9: Mainfield
        10: Headland
        11: BufferZone
        12: Windbreak
    """
    def __init__(self, type):
        self.type = type
        self.et = ET.Element("PLN", A=str(self.type))

    def add_linestring(self, linestring):
        self.et.append(linestring.et)


class Linestring:
    """
    Types:
        1: PolygonExterior
        2: PolygonInterior
        3: TramLine
        4: SamplingRoute
        5: GuidancePattern
        6: Drainage
        7: Fence
        8: Flag
        9: Obstacle
    """
    def __init__(self, type):
        self.type = type
        self.et = ET.Element("LSG", A=str(self.type))

    def add_point(self, point):
        self.et.append(point.et)


class Point:
    """
    Types:
        1: Flag
        2: other
        3: Field Access
        4: Storage
        5: Obstacle
        6: Guidance Reference A
        7: Guidance Reference B
        8: Guidance Reference Center
        9: Guidance Point
        10: Partfield Reference Point
        11: Homebase
    """
    def __init__(self, type, north, east):
        self.type = str(type)
        self.north = str(round(north, 9))
        self.east = str(round(east, 9))
        self.et = ET.Element("PNT", A=self.type, C=self.north, D=self.east)


class Task:

    """
    Task Status = 1 (Planned)
    """
    def __init__(self, id: int, designator, status=1):
        self.id = f"TSK-{id}"
        self.designator = designator
        self.status = str(status)
        self.et = ET.Element("TSK", A=self.id, B=self.designator, G=self.status)

    def add_grid(self, grid):
        self.et.append(grid.et)

    def add_treatment_zone(self, treatment_zone):
        self.et.append(treatment_zone.et)

    def add_worker_allocation(self, worker_allocation):
        self.et.append(worker_allocation.et)

    def set_partfield(self, partfield):
        self.et.set("E", partfield.id)

    def set_customer(self, customer):
        self.et.set("C", customer.id)

    def set_farm(self, farm):
        self.et.set("D", farm.id)


class Grid:

    def __init__(self, minimum_north, minimum_east, cell_north_size, cell_east_size, max_column, max_row, filename, type, treatment_zone_code=None):
        self.minimum_north = str(round(minimum_north, 9))
        self.minimum_east = str(round(minimum_east, 9))
        self.cell_north_size = str(round(cell_north_size, 9))
        self.cell_east_size = str(round(cell_east_size, 9))
        self.max_column = str(max_column)
        self.max_row = str(max_row)
        self.filename = str(filename)
        self.type = str(type)
        self.treatment_zone_code = treatment_zone_code
        self.et = ET.Element("GRD", A=self.minimum_north, B=self.minimum_east, C=self.cell_north_size, D=self.cell_east_size,
            E=self.max_column, F=self.max_row, G=self.filename, I=self.type)

        if self.treatment_zone_code:
            self.set_treatment_zone_code(self.treatment_zone_code) 

    def set_treatment_zone_code(self, treatment_zone):
        self.treatment_zone_code = treatment_zone.zone_code
        self.et.set("J", self.treatment_zone_code)


class GuidanceGroup:
    def __init__(self, id: int, designator):
        self.id = f"GGP-{id}"
        self.designator = str(designator)
        self.et = ET.Element("GGP", A=self.id, B=self.designator)

    def add_guidance_pattern(self, guidance_pattern):
        self.et.append(guidance_pattern.et)


class GuidancePattern:
    
    """
    Types: 
        1: AB
        2: A+
        3: Curve
        4: Pivor
        5: Spiral
    """
    def __init__(self, id: int, type: int, propagation_direction=1, extension=1):
        self.id = f"GPN-{id}"
        self.type = str(type)
        self.extension = str(extension)
        self.propagation_direction = str(propagation_direction)
        self.et = ET.Element("GPN", A=self.id, C=self.type, E=self.propagation_direction, F=self.extension)

    def add_linestring(self, linestring):
        self.et.append(linestring.et)


class TreatmentZone:

    def __init__(self, zone_code: int):
        self.zone_code = str(zone_code)
        self.et = ET.Element("TZN", A=self.zone_code)

    def add_process_data_variable(self, process_data_variable):
        self.et.append(process_data_variable.et)


class ProcessDataVariable:

    def __init__(self, process_data_ddi: str, process_data_value=0, value_presentation_id_ref=None):
        self.process_data_ddi = process_data_ddi
        self.process_data_value = str(process_data_value)
        self.value_presentation_id_ref = value_presentation_id_ref
        self.et = ET.Element("PDV", A=self.process_data_ddi, B=self.process_data_value)

        if self.value_presentation_id_ref:
            self.set_value_presentation_id_ref(self.value_presentation_id_ref)


    def set_value_presentation(self, value_presentation):
        self.value_presentation_id_ref = str(value_presentation.id)
        self.et.set("E", self.value_presentation_id_ref)


class ValuePresentation:

    def __init__(self, id: int, scale, unit_designator: str, number_of_deciamls=2, offset=0):
        self.id = f"VPN-{id}"
        self.scale = str(scale)
        self.unit_designator = unit_designator
        self.number_of_deciamls = str(number_of_deciamls)
        self.offset = str(offset)
        self.et = ET.Element("VPN", A=self.id, B=self.offset, C=self.scale, D=self.number_of_deciamls, E=self.unit_designator)


class Worker:
    
    def __init__(self, id: int, lastname: str, firstname=None):
        self.id = f"WKR-{id}"
        self.lastname = lastname
        self.firstname = firstname
        self.et = ET.Element("WKR", A=self.id, B=self.lastname)

        if self.firstname:
            self.et.set("C", self.firstname)

class WorkerAllocation:

    def __init__(self, worker_id_ref):
        self.worker_id_ref = str(worker_id_ref)
        self.et = ET.Element("WAN", A=worker_id_ref)


class Customer:

    def __init__(self, id: int, lastname: str):
        self.id = f"CTR-{id}"
        self.lastname = lastname
        self.et = ET.Element("CTR", A=self.id, B=self.lastname)


class Farm:

    def __init__(self, id: int, designator: str):
        self.id = f"FRM-{id}"
        self.designator = designator
        self.et = ET.Element("FRM", A=self.id, B=self.designator)
