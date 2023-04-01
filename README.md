# Django WebSocket Chat

<img src="https://assets.stanko.io/blog/production/store/a6bad9b68057b2ed9716dd35ced216fa.gif">

WebSocket Chat is a real-time chat application that allows people to converse with each other in one-to-one messages using the WebSocket protocol.

## Features

- Real-time one-to-one messaging
- Responsive design for all devices
- Ability to send text messages, emojis, and images
- Simple and intuitive interface
- User authentication and authorization
- Support for multiple chat rooms
- Secure communication using HTTPS and WSS protocols

## Getting Started

To get started with WebSocket Chat, follow these steps:

1. Clone the repository using the command `git clone https://github.com/xolmomin/drf_channel.git`
2. Navigate to the project directory using the command `cd drf_channel`
3. Install the dependencies using the command `pip install -r requirements.txt`
4. Start the server using the command `python manage.py runserver`
5. Open your web browser and go to `http://localhost:8000`


## Usage

<img src="https://blog.postman.com/wp-content/uploads/2021/05/websocket-connect-1.gif">

To use WebSocket Chat, follow these steps:
1. Enter your POSTMAN and crate websocket folloving press `CTRL + N`.
2. Once you're entered, you'll be enter websocket url like `ws://localhost:8000/ws`.
3. Click on a user's name to start a one-to-one conversation with them.
4. Type your message in the input box at the bottom of the screen and hit enter to send it.
5. You can also send emojis and images by clicking on the corresponding buttons above the input box.

## Contributing

If you'd like to contribute to WebSocket Chat, please follow these steps:

1. Fork the repository on GitHub.
2. Clone your forked repository using the command `git clone https://github.com/xolmomin/drf_channel.git`
3. Create a new branch for your changes using the command `git checkout -b my-new-feature`
4. Make your changes to the code and test them locally.
5. Commit your changes using the command `git commit -m 'Add some feature'`
6. Push your changes to your forked repository using the command `git push origin my-new-feature`
7. Create a pull request on GitHub.

## Credits

WebSocket Chat was created by Your Name. It uses the following open-source software:

### Main
- Python
- Django
- Websocket
- Rest API
- Postgresql

### Required
- django = "4.0.8"
- djangorestframework = "3.12.4"
- djangorestframework-simplejwt = "4.8.0"
- channels = "3.0.4"

## License

WebSocket Chat is licensed under the MIT License. See `LICENSE` for more information.

user
- is_online
- last_activity

per to per chat
- message
    - edit
    - delete
    - is_read
    - send file
    - block
    - 
group
- views





testing



 - 1ta gruppa ochib ichida yozish
 - har biriga alohida gruppa ochib yuborish



TASKs

- README.md
- fayllarni bo'laklash
- /get-chat-list (oldin barcha yozilgan userlar listi) [API]
- 1ta userga tegishli message larni olish pagination bilan [API]
- msg edit qilish, send file, last_activity

- https://serpy.readthedocs.io/en/latest/performance.html serializer larni togrilash
- testing

