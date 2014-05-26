import pymongo, re
from pymongo import MongoClient, ASCENDING, DESCENDING


pattern = re.compile(r"(\d+)_(\d)_(\d+)([A-Z]?)\D*$")


def process_match(match):
    if match:
        route = match.group(1)
        dir = match.group(2)
        if route != match.group(3):
            return None
        branch = match.group(4)
        if branch == 'S':
            branch = ''
        return route, dir, branch
    else:
        return None


def extract_rdb(tag):
    match = pattern.match(tag)
    return process_match(match)


def create_regex(route, dir, branch):
    return re.compile(r"^%s_%s_%s%s\D*$" % (route, dir, route, branch))


if __name__ == '__main__':
    client = MongoClient()
    db = client.datasummative
    directions = db.directions
    directions_norm = db.directions_norm
    for direction in directions.find():
        tag = direction['tag']
        name = direction['name']
        title = direction['title']
        matched = extract_rdb(tag)
        print(direction)
        if matched:
            route, dir, branch = matched
            doc = {'route': route,
                   'dir': dir,
                   'branch': branch,
                   'name': name,
                   'title': title}
            spec = {'route': route, 'dir': dir, 'branch': branch}
            directions_norm.update(spec, doc, upsert=True)
