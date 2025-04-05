# Chatbot

Just implement the `on_message` function in `main.py` and Chatbot will take care of the rest :)

File textbase is the backend and Chatbot to send is frontend

## Frontend
### `npm run build`

Builds the app for production to the `build` folder.\
It correctly bundles React in production mode and optimizes the build for the best performance.

The build is minified and the filenames include the hashes.\
The app is ready to be deployed!


## Installation

Clone the repository and install the dependencies using [Poetry](https://python-poetry.org/) (you might have to [install Poetry](https://python-poetry.org/docs/#installation) first).

You'd better create a conda virtual environment before using poetry.

```bash
poetry install
```

```bash
poetry run python textbase/textbase_cli.py test main.py
```

Now go to [http://localhost:4000](http://localhost:4000) and start chatting with your bot! The bot will automatically reload when you change the code.

