# Date formats

In this program, two date formats are used:

1. `YY-mm-dd` - standard ISO 8601 format. Prefered **input** format. Use this style in your `PUT` and `POST` requests.

2. `dd.mm.YY` - russian format. Sometimes accepted as input, sometimes not (I'm working on fixing this, but for now, only ISO 8601 will work for all cases). All **output data** (which is usually received from `GET` requests) will be formatted to this output.
