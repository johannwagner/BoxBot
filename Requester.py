import requests

import Security


def get_rate_limit():
    request = requests.get("https://api.github.com/rate_limit",
                           params={"client_id": Security.CLIENT_ID,
                                   "client_secret": Security.CLIENT_SECRET}).json()
    rate = request.get("rate")

    return {'actual': rate.get('remaining'),
            'all': rate.get('limit')}

def get_comment_stats():
    request = requests.get("https://api.github.com/repos/hovgaardgames/startupcompany/issues/comments",
                           params={"client_id": Security.CLIENT_ID,
                                   "client_secret": Security.CLIENT_SECRET,
                                   "per_page": 100,
                                   "sort": "created",
                                   "direction": "desc"
                                   }).json()
    return request

def get_milestone_stats():
    request = requests.get("https://api.github.com/repos/hovgaardgames/startupcompany/milestones",
                           params={"client_id": Security.CLIENT_ID,
                                   "client_secret": Security.CLIENT_SECRET}).json()

    return [{"title": milestone['title'],
             "open": milestone['open_issues'],
             "closed": milestone['closed_issues'],
             "all": int(milestone['open_issues']) + int(milestone['closed_issues']),
             "percentage": int(milestone['closed_issues']) * 100/ (int(milestone['open_issues']) + int(milestone['closed_issues']))} for milestone in request]


def get_issue_stats():
    request = requests.get("https://api.github.com/repos/hovgaardgames/startupcompany/issues",
                           params={"state": "all",
                                   "client_id": "6155522b016d8c49ce3a",
                                   "client_secret": "75d08f6977075855c730a406e93c96774a386769",
                                   "per_page": 100})
    json = request.json()
    return json