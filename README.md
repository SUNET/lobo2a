
Lobo2 ARIA driver
=================

A simple application demonstrating the lobo2 API. This is very rudamentary software. You are probably better off
looking at the source as an example rather than using this as a tool right now. If do do decide to play with lobo2a
then start aria2c using something like the provided start-aria.sh script.

Development Installation
------------

# create & activate virtualenv
# setup.py develop
# lobo2 --help

Usage
-----

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

Example
-------

# env LOBO2URL=http://localhost:8000 lobo2a -d /tmp recv <info_hash_hex>
# env LOBO2URL=http://localhost:8000 LOBO2TOKEN=<bearer token> lobo2a send file_or_directory