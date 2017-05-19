# Gitter Mention LED

This script will listen in on a gitter room, and light up an LED when the selected username gets mentioned.
The script only tracks the last mention, to limit calls to the API.

Use your personal token for the token, as this is needed to automatically clear the unread status

Find your token [here](https://developer.gitter.im/apps)  

To install, first enter the gitterest directory. Run

    sudo python3 setup.py install
    sudo pip3 install RPIO

Then go back to the main directory, and set up the systemd service to have it start on boot:

    sudo cp gitterLED.service /lib/systemd/system/gitterLED.service
    sudo chmod 644 /lib/systemd/system/gitterLED.service
    sudo systemctl enable gitterLED.service
    sudo systemctl start gitterLED

I might have missed some dependencies, but feel free to submit an issue if that's the case.

Here's a [video](https://www.youtube.com/watch?v=7hQOwxnkIEM) of the thing in action, and a long blabber about the code.
