import enum
from typing import Dict, Any


def legend_title(title: str, subtitle: str, has_divider: bool) -> Dict[str, Any]:
    return {
        "widget_type": "LEGEND_TITLE_ROW",
        "data": {
            "@type": "type.googleapis.com/widgets.LegendTitleRowData",
            "title": title,
            "subtitle": subtitle,
            "has_divider": True,
            "image_url": "logo"
        }
    }


def group_info(data_map: Dict[str, str] = None) -> Dict[str, Any]:
    items = []
    for key, value in data_map.items():
        items.append({
            "title": key,
            "value": value
        })
    return {
        "widget_type": "GROUP_INFO_ROW",
        "data": {
            "@type": "type.googleapis.com/widgets.GroupInfoRow",
            "items": items,
            "has_divider": True
        }
    }


def score_row(title: str, percentage_score: int, score_color: str, has_divider: bool) -> Dict[str, Any]:
    return {
        "widget_type": "SCORE_ROW",
        "data": {
            "@type": "type.googleapis.com/widgets.ScoreRowData",
            "title": title,
            "percentage_score": percentage_score,
            "score_color": score_color,
            "hasDivider": has_divider,
            "icon": {
                "icon_name": "HISTORY",
            }
        }
    }


def evaluation_section(text: str, text_color: str, section_color: str) -> Dict[str, Any]:
    return {
        "text": text,
        "text_color": text_color,
        "section_color": section_color
    }


def evaluation_row(indicator_percentage: int) -> Dict[str, Any]:
    evaluation_text = {
        0: "ضعیف",
        1: "نسبتا ضعیف",
        2: "متوسط",
        3: "نسبتا خوب",
        4: "خوب"
    }
    indicator_text = evaluation_text[min((indicator_percentage // 20), 4)]
    return {
        "widget_type": "EVALUATION_ROW",
        "data": {
            "@type": "type.googleapis.com/widgets.EvaluationRowData",
            "indicator_text": indicator_text,
            "indicator_percentage": indicator_percentage,
            "indicator_icon": {
                "image_url_dark": "",
                "image_url_light": "",
                "icon_name": "ADD",
                "icon_color": "BRAND_PRIMARY"
            },
            "indicator_color": "BRAND_PRIMARY",
            "left": evaluation_section(text="ضعیف", text_color="ICON_PRIMARY"
                                       , section_color="ERROR_PRIMARY"),
            "middle": evaluation_section(text="متوسط", text_color="ICON_PRIMARY"
                                         , section_color="WARNING_PRIMARY"),
            "right": evaluation_section(text="خوب", text_color="ICON_PRIMARY"
                                        , section_color="SUCCESS_PRIMARY")
        }
    }
