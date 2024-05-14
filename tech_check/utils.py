import requests

from kenar_example import settings
from misc.wigets import legend_title, group_info, score_row, evaluation_row


def apply_report_in_divar(report) -> requests.Response:
    post = report.post
    total_evaluation = sum([
        report.battery_health,
        report.screen_health,
        report.camera_health,
        report.body_health,
        report.performance_health
    ]) / 5
    response = requests.post(settings.DIVAR_OPEN_PLATFORM_BASE_URL + f'/add-ons/post/{post.token}', headers={
        'content-type': 'application/json',
        'x-api-key': settings.DIVAR_API_KEY,
        'x-access-token': post.access_token,
    }, json={
        'widgets': {
            'widget_list': [
                legend_title(title="TechCheck Mobile", subtitle="کارشناسی گوشی موبایل", has_divider=True),
                group_info({
                    "سلامت باتری": f"{report.battery_health}%",
                    "سلامت صفحه نمایش": f"{report.screen_health}%",
                    "سلامت دوربین": f"{report.camera_health}%",

                }),
                score_row(title="سلامت بدنه", percentage_score=report.body_health
                          , score_color="SUCCESS_PRIMARY", has_divider=True),
                score_row(title="سلامت پردازنده", percentage_score=report.performance_health
                          , score_color="SUCCESS_PRIMARY", has_divider=True),
                evaluation_row(int(total_evaluation))
            ]
        },
        "semantic": {
            "year": "1398",
            "usage": "100000"
        },
        "notes": "any notes you want to get back on list api"
    })
    return response
