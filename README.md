# Southwest-Airlines-Flights
This project will aggregate the cheapest round-trip flights on given dates from a given departure airport, outputting a sorted csv that will be automatically emailed to desired recipients.

**Southwest.py no longer works; permission denied by Southwest Airline's website when using selenium get() function to perform search, a new approach is currently being resolved**

## Required Inputs
  #### search_params.py Inputs:
  * Departure Airport (three letter airport code)
  * Departure Date (YYYY-MM-DD)
  * Return Date (YYYY-MM-DD)
  #### send_email.py Inputs:
  * fromaddr (sender's email)
  * toaddr (all recipient's emails)
  * attachment (path to sorted csv)
  * pw (sender's email password)
