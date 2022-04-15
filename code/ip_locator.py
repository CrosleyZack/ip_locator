# encoding=utf8
# Author: crosleyzack

from flask import Flask, redirect, url_for, request, render_template
import geoip2.webservice
import geoip2.errors

# Setup Flask App. Use the file name for ease.
app = Flask(__name__)

# app name
@app.errorhandler(404)
def not_found(e):
    '''
    Handle 404 errors.
    '''
    return render_template("error.html")

@app.route('/invalid/<ip>')
def invalid(ip):
    '''
    Handle invalid IP addresses.

    :param ip: the invalid IP address which caused the query to fail.
    :type ip: str
    :returns: A web page with a basic string indicating the IP was not locatable.
    '''
    # NOTE: this just prints on page whatever is passed on in Lat and Lon. This is
    #       100% an XSS vulnerability. I would _never_ do this in production code.
    #       DISCLAIMER: As a caveat, my website does have a hidden XSS vulnerability
    #                   intentionally as part of a hidden game I built into it. So
    #                   I would never do something to introduce an XSS vulnerability
    #                   "unintentionally".
    return f'The provided ip {ip} is reserved or invalid and cannot be located.'

@app.route('/location/<lat>:<lon>')
def location(lat, lon):
    '''
    Display the latitude and longitude associated with the provided IP address.

    :param lat: the Latitude (approximate) of the IP address.
    :type lat: str
    :param lon: the Longitude (approximate) of the IP address.
    :type lon: str
    :returns: A web page indicating the latitude and longitude of the IP address.
    '''
    # NOTE: Obviously this would be much better if done as an asynchronous service
    #   where it would show up on the /input page after an asynchronous call,
    #   instead of going to a new page. This was simply done for ease. If I
    #   were making a production website, I would do it asynchronously.
    # NOTE: this just prints on page whatever is passed on in Lat and Lon. This is
    #       100% an XSS vulnerability. I would _never_ do this in production code.
    #       DISCLAIMER: As a caveat, my website does have a hidden XSS vulnerability
    #                   intentionally as part of a hidden game I built into it. So
    #                   I would never do something to introduce an XSS vulnerability
    #                   "unintentionally".
    return f'Latitude: {lat}\nLongitude: {lon}'


@app.route('/input', methods=['POST', 'GET'])
def input():
    '''
    Web page to get input IP address to locate from the user.
    '''
    if request.method == 'POST':
        # NOTE: this just grabs whatever is in the IP form field. This shouldn't
        #       enable an XSS attack since it just gets piped into the query to
        #       geoip2, but it should still be sanitized.
        ip_addr = request.form['ip']
        # NOTE: These values should never be in plain text. They also should
        #       never be on the host computer. If this were being made for
        #       production, these values should be encrypted in a database
        #       where only the server can access them, and all requests to this
        #       API point would be done through the server side. Having it here
        #       is a shortcut I took for this, and fortunately these requests
        #       do not cost me any money if someone uses the id and license
        #       for themselves :-)
        user_id = 706902
        license = b'7ANP1iJ70CPEUcdn'
        # Query the geoip2 service to get the latitude and longitude. If this
        #   query fails, load the error page.
        with geoip2.webservice.Client(user_id, license, host='geolite.info') as client:
            try:
                response = client.city(ip_addr)
            except (geoip2.errors.AddressNotFoundError, ValueError):
                return redirect(url_for('invalid', ip=ip_addr))
        # Extract lat-lon and display.
        latitude = response.location.latitude
        longitude = response.location.longitude
        return redirect(url_for('location', lat=latitude, lon=longitude))
    else:
        return render_template('input.html')
    #     ip_addr = request.args.get('ip')
    #     return redirect(url_for('location', ip=ip_addr))


@app.route('/')
def home():
    '''
    Redirect the main url to my input page. This is just for ease of use.
    '''
    return redirect('/input')


if __name__ == '__main__':
    app.run(debug = True)