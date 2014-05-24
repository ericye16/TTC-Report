import pymongo, re
from pymongo import MongoClient, ASCENDING, DESCENDING


if __name__ == '__main__':
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

    client = MongoClient()
    db = client.datasummative
    directions = db.directions
    directions_norm = db.directions_norm
    for direction in directions.find():
        tag = direction['tag']
        name = direction['name']
        title = direction['title']
        match = re.match(pattern, tag)
        matched = process_match(match)
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
