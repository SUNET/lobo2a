#!/bin/bash

aria2c --enable-rpc --seed-ratio=0.0 --force-save=true --allow-overwrite=true --check-integrity=true --bt-hash-check-seed=true --dir=/tmp --rpc-save-upload-metadata=true --save-session=session.dat --save-session-interval=30 --input-file=session.dat --auto-file-renaming=false