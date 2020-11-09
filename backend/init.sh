#!/bin/bash

redis-server &
python -m ducts server start
/bin/bash
