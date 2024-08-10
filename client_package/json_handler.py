import json
import os

def save_to_json(slides_summary, pptx_filename):
    """
    Saves the slides summary to a json file using the basename of the pptx file.
    :param slides_summary: a list of slides summary
    :param pptx_filename: the filename of the pptx
    """

    # create the json structor, for each slide pin its number and its content separately
    structured_slides = [
        {"slide_number": i + 1, "content": content} for i, content in enumerate(slides_summary)
    ]

    # structure all the slides togather
    structured_data = {
        "presentation": os.path.basename(pptx_filename),
        "slides": structured_slides
    }

    # change filename from .pptx to .json
    base_name = os.path.splitext(pptx_filename)[0]
    json_file = base_name + '.json'

    # save as json
    with open(json_file, 'w') as f:
        json.dump(structured_data, f, indent=4)