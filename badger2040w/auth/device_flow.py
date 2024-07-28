import badger2040
import jpegdec
import urequests
import qrcode
import time

from badger2040 import WIDTH, HEIGHT


display = badger2040.Badger2040()
display.led(128)
display.set_update_speed(2)

jpeg = jpegdec.JPEG(display.display)

DARKEST = 15

LIGHTEST = 0


def measure_qr_code(size, code):
    w, h = code.get_size()
    module_size = int(size / w)
    return module_size * w, module_size


def draw_qr_code(ox, oy, size, code):
    size, module_size = measure_qr_code(size, code)
    display.set_pen(LIGHTEST)
    display.rectangle(ox, oy, size, size)
    display.set_pen(DARKEST)
    for x in range(size):
        for y in range(size):
            if code.get_module(x, y):
                display.rectangle(ox + x * module_size, oy + y * module_size, module_size, module_size)


def draw_page(data):
    # Clear the display
    display.set_pen(15)
    display.clear()
    display.set_pen(0)

    # Draw the page header
    display.set_font("bitmap6")
    display.set_pen(0)
    display.rectangle(0, 0, WIDTH, 20)
    display.set_pen(15)
    display.text("Device Authz Flow", 3, 4)
    display.set_pen(0)

    display.set_font("bitmap8")

    display.set_pen(0)
    display.text("User code received.", 3, 28, WIDTH - 105, 2)
    display.text(f"Code: {data['user_code']}", 3, 48, WIDTH - 105, 2)
    
    # Draws QR Code from URI
    display.set_pen(DARKEST)
    code = qrcode.QRCode()
    code.set_text(data['verification_uri_complete'])

    size, module_size = measure_qr_code(HEIGHT, code)
    draw_qr_code(196, 24, HEIGHT, code)
    
    display.update()


def login(auth0_request_data):
    """
    Runs the device authorization flow and stores the user object in memory
    """

    device_code_data = (f"client_id={auth0_request_data['client_id']}" +
        f"&scope=openid profile" +
        f"&audience={auth0_request_data['audience']}"
    )
    
    headers = {
        "Content-Type": "application/x-www-form-urlencoded"
    }
    url = "https://{}/oauth/device/code".format(
        auth0_request_data['domain'])
    device_code_response = urequests.post(
        url,
        headers=headers,
        data=device_code_data
    )
    
    if device_code_response.status_code != 200:
        print('Error generating the device code')
        return
        # raise typer.Exit(code=1)

    print('Device code successful')
    data = device_code_response.json()
    print('1. On your computer or mobile device navigate to: ', data['verification_uri_complete'])
    print('2. Enter the following code: ', data['user_code'])
    draw_page(data)
    print(data)

    grant_type = 'urn:ietf:params:oauth:grant-type:device_code'
    device_code_data = (f"device_code={data['device_code']}" +
        f"&client_id={auth0_request_data['client_id']}" +
        f"&grant_type={grant_type}"
    )
    headers = {
        "Content-Type": "application/x-www-form-urlencoded"
    }
    url = "https://{}/oauth/token".format(
        auth0_request_data['domain'])
    user_confirmation = False
    elapsed_time = 0
    while not user_confirmation:
        # Test for user confirmation until token expires in intervals
        # from the device code
        
        # Request tokens from Auth0 to call protected API
        token_response = urequests.post(
            url,
            headers=headers,
            data=device_code_data
        )
        tokens = token_response.json()
        
        if 'error' in tokens.keys() and elapsed_time <= data["expires_in"]:
            elapsed_time += data["interval"]  # increase interval time
            time.sleep(data["interval"])
            print(f"Time till expiration {data['expires_in'] - elapsed_time}")
            
        else:
            user_confirmation = True
    
    # Return tokens to application
    return tokens 
