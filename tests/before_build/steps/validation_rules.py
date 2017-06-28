
def validate_event(event):
    from validator import *

    archive_rules = {
        "archive": [Required, {
            "photos_url": [Required, Truthy()],
            "videos_url": [Required, Truthy()],
        }]
    }
    overview_rules = {
        "overview": [Required, {
            "left_content": [Required, Truthy()],
            "right_content": [Required, Truthy()],
        }]
    }
    event_rules = {
        "layout": [Required, Truthy()],
        "title": [Required, Truthy(), Length(0, maximum=80)],
        "subtitle": [Required, Truthy(), Length(0, maximum=80)],
        "datelocation": [Required, Truthy(), Length(0, maximum=80)],
        "archive": [
            If(Truthy(), Then(archive_rules))
        ],
        "overview": [
            If(Truthy(), Then(overview_rules))
        ]
    }
    return validate(event_rules, event)
