# Password_Manager

A **Streamlit** app to manage Passwords.

## Dependencies

* First of all, make sure that you have these pip packages:

        mysql-connector-python
        python-dotenv
        streamlit

## Installation

* After that, create a **.env** file, setting the variables:

        touch .env
        echo 'DB_PORT=3306' >> .env
        echo 'DB_HOSTNAME=localhost' >> .env
        echo 'DB_USER=root' >> .env
        echo 'DB_NAME=seguranca' >> .env
        echo 'DB_PASSWORD=password' >> .env

* Create service:

        sudo cp services/pmscript.sh /usr/bin/
        sudo nano /usr/bin/pmscript.sh 

        * Change $USER by your username.

        sudo cp services/pmscript.service /lib/systemd/system
        sudo systemctl enable pmscript.service
        sudo systemctl daemon-reload
        sudo systemctl start pmscript.service
