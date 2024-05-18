class DDI:

    def __init__(self, ddi_id, definition, unit_symbol, bit_resolution):
        self.definition = definition
        self.unit_symbol = unit_symbol
        self.bit_resolution = bit_resolution
        self.ddi_id = ddi_id
        self.ddi_id_hex = '{:04x}'.format(ddi_id).upper()


    @staticmethod
    def _get_from_ddi_id(ddi_id):
        data = ddi_data.get(ddi_id)
        return DDI(ddi_id, data["definition"], data["unit_symbol"], data["bit_resolution"])


    @staticmethod
    def setpoint_volume_per_area_application_rate():
        return DDI._get_from_ddi_id(1)


    @staticmethod
    def setpoint_mass_per_area_application_rate():
        return DDI._get_from_ddi_id(6)


    @staticmethod
    def setpoint_count_per_area_application_rate():
        return DDI._get_from_ddi_id(11)



ddi_data = {
    1: {
        "definition": "Setpoint Application Rate specified as volume per area as [mm³/m²]",
        "unit_symbol": "mm³/m²",
        "bit_resolution": 0.01
    },
    6: {
        "definition": "Setpoint Application Rate specified as mass per area",
        "unit_symbol": "mg/m²",
        "bit_resolution": 1
    },
    11: {
        "definition": "Setpoint Application Rate specified as count per area",
        "unit_symbol": "/m²",
        "bit_resolution": 0.001
    },
    16: {
        "definition": "Setpoint Application Rate specified as distance: e.g. seed spacing of a precision seeder",
        "unit_symbol": "mm",
        "bit_resolution": 1
    },
    21: {
        "definition": "Setpoint Application Rate specified as volume per volume",
        "unit_symbol": "mm³/m³",
        "bit_resolution": 1
    },
    51: {
        "definition": "Setpoint Tillage Depth of Device Element below soil surface, value increases with depth. In case of a negative value the system will indicate the distance above the ground.",
        "unit_symbol": "mm",
        "bit_resolution": 1
    },
    56: {
        "definition": "Setpoint Seeding Depth of Device Element below soil surface, value increases with depth",
        "unit_symbol": "mm",
        "bit_resolution": 1
    },
    
}
