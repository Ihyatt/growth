from app.models.medication import Medication
from app.models.report import Report


def get_resource_model(resource_type_str):

    resource_models_map = {
        'medication': Medication,
        'report': Report,
    }
    
    model = resource_models_map.get(resource_type_str.lower())
    
    if not model:
        abort(400, description=f"Invalid resource type: '{resource_type_str}'")
        
    return model
