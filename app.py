import flask
import sys

from block import block

block.run(port=8000, debug=True, host='0.0.0.0')