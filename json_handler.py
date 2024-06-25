import json
import os

def save_to_json(slides_summary, pptx_filename):
    """
    Saves the slides summary to a json file using the basename of the pptx file.
    :param slides_summary: a list of slides summary
    :param pptx_filename: the filename of the pptx
    """

    # change filename from .pptx to .json
    base_name = os.path.splitext(pptx_filename)[0]
    json_file = base_name + '.json'

    # save as json
    with open(json_file, 'w') as f:
        json.dump(slides_summary, f, indent=4)