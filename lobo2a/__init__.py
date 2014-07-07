"""
Usage: lobo2a [-d|--storage directory] [-u|--rpcurl aria2 RPC endpoint] [-h|--help] [-v|--version] <cmd> <parameters>

Uses aria2c RPC to interface with a lobo2 instance. The default lobo2 instance is defined in the LOBO2URL
environment variable (must be present).

Commands:

   list
        display current datasets & status
   del <dataset ID> (<dataset ID> *)
        removes dataset(s) except data
   recv <dataset ID> (<dataset ID> *)
        receive dataset(s) by ID
   send <dir|file>
        creates new dataset from file or directory and send

"""
import StringIO
import hashlib

import sys
import getopt
import feedparser
import pkg_resources
import xmlrpclib
import os
import requests
from torrenttools import make_meta_file, bdecode, bencode

__version__ = pkg_resources.require("lobo2a")[0].version
__author__ = 'leifj'


def _list_all(s):
    lst = []
    lst.extend(s.aria2.tellActive(['gid', 'infoHash']))
    #lst.extend(s.aria2.tellWaiting(['gid', 'infoHash']))
    #lst.extend(s.aria2.tellStopped(['gid', 'infoHash']))
    return lst


def main():
    """
    The main entrypoint for the lobo2a cmdline tool.
    """
    try:
        opts, args = getopt.getopt(sys.argv[1:], 'hu:d:', ['help', 'version', 'rpcurl', 'storage'])
    except getopt.error, msg:
        print msg
        print 'for help use --help'
        sys.exit(2)

    rpcurl = "http://localhost:6800/rpc"
    storage = '/tmp'
    piece_length = 65535
    for o, a in opts:
        if o in ('-h', '--help'):
            print __doc__
            sys.exit(0)
        elif o in ('-u', '--rpcurl'):
            rpcurl = a
        elif o in '--version':
            print "pyff version %s" % __version__
            sys.exit(0)
        else:
            raise ValueError("Unknown option '%s'" % o)

    if 0 == len(args):
        print __doc__
        sys.exit(1)

    if not 'LOBO2URL' in os.environ:
        print "no LOBO2URL in environment"
        print __doc__
        sys.exit(1)

    lobo2url = os.environ['LOBO2URL']
    lobo2token = os.environ.get('LOBO2TOKEN', None)

    s = xmlrpclib.ServerProxy(rpcurl)

    if args[0] == 'list':
        print _list_all(s)
    elif args[0] == 'del':
        for did in args[1:]:
            for dl in dls:
                if 'infoHash' in dl and dl['infoHash'] == did:
                    s.aria2.remove(dl['gid'])
    elif args[0] == 'feed':
        active = dict([(a['infoHash'], a['gid']) for a in _list_all(s)])
        if args[1] == 'recent':
            recent = feedparser.parse("%s/feeds/recent.rss" % lobo2url)
            dls = _list_all(s)
            for item in recent.entries:
                if not item.title in active:
                    s.aria2.addUri([item.link], dict(dir=storage))
    elif args[0] == 'recv':
        print s.aria2.addUri(["%s/api/dataset/%s.torrent" % (lobo2url, did) for did in args[1:]], dict(dir=storage))
    elif args[0] == 'send':
        if lobo2token is None:
            print "no LOBO2TOKEN in environment - you need to authenticate to %s to send datasets" % lobo2url
            sys.exit(1)
        src = args[1]
        buf = StringIO.StringIO()
        make_meta_file(src, "%s/announce" % lobo2url, piece_length, title=os.path.basename(src), target=buf)
        tdf = buf.getvalue()
        buf.seek(0)
        torrent_data = bdecode(tdf)
        info_hash = hashlib.sha1(bencode(torrent_data['info'])).hexdigest()
        r = requests.post("%s/api/dataset" % lobo2url,
                          files=dict(torrent=("%s.torrent" % info_hash, buf, 'application/x-bittorrent', {})),
                          headers=dict(authorization="Bearer %s" % lobo2token,
                                       accept='application/json'))
        print r.text
        if r.status_code != requests.codes.ok:
            sys.exit(2)
        print s.aria2.addUri(["%s/api/dataset/%s.torrent" % (lobo2url, info_hash)], dict(dir=os.path.dirname(src)))
    else:
        print "unknown command %s" % args[0]
        print __doc__
        sys.exit(1)