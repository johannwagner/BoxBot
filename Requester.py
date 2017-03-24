import requests

import Security


def get_rate_limit():
    request = requests.get("https://api.github.com/rate_limit",
                           params={"client_id": Security.CLIENT_ID,
                                   "client_secret": Security.CLIENT_SECRET}).json()
    rate = request.get("rate")

    return {'actual': rate.get('remaining'),
            'all': rate.get('limit')}

def get_milestone_stats():
    request = requests.get("https://api.github.com/repos/hovgaardgames/startupcompany/milestones",
                           params={"client_id": Security.CLIENT_ID,
                                   "client_secret": Security.CLIENT_SECRET}).json()

    return [{"title": milestone['title'],
             "open": milestone['open_issues'],
             "closed": milestone['closed_issues'],
             "all": int(milestone['open_issues']) + int(milestone['closed_issues']),
             "percentage": int(milestone['open_issues']) * 100/ (int(milestone['open_issues']) + int(milestone['closed_issues']))} for milestone in request]
