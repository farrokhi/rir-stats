import re


def normalize(s):
    ret = re.sub('[\|\"\']', ' ', s)
    ret = re.sub('route object', '', ret, flags=re.IGNORECASE)
    return ret


def dumproutes(inputfile, outputfile):
    infp = open(inputfile, 'r', encoding='ISO-8859-1')
    outfp = open(outputfile, 'wt', encoding='UTF8')

    print("%s -> %s ..." % (inputfile, outputfile))

    route = {}
    reroute = re.compile('^route\:\s*(.+)$')
    redescr = re.compile('^descr\:\s*(.+)$')
    reorigin = re.compile('^origin\:\s*(.+)$')

    for line in infp:
        if line == '\n':
            if route.get('route', None) is not None:
                r = route.get('route', '').strip()
                d = route.get('descr', '').strip()
                o = route.get('origin', '').strip()
                s = str.format("%s|%s (%s)\n" % (r, d, o))
                outfp.write(s)
            route = {}
            continue

        if line.startswith('route:'):
            p = reroute.match(line)
            if p:
                route['route'] = p.group(1)

        if line.startswith('origin:'):
            p = reorigin.match(line)
            if p:
                route['origin'] = p.group(1)

        if line.startswith('descr:') and route.get('descr', None) is None:
            p = redescr.match(line)
            if p:
                route['descr'] = normalize(p.group(1))

    infp.close()
    outfp.close()


if __name__ == '__main__':
    dumproutes('arin.db', 'output/arin.csv')
    dumproutes('afrinic.db', 'output/afrinic.csv')
    dumproutes('apnic.db.route', 'output/apnic.csv')
    dumproutes('ripe.db.route', 'output/ripe.csv')