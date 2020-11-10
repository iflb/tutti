#!/bin/bash

rm -rf ./.pid
redis-server &
python -m ducts server start
/bin/bash
