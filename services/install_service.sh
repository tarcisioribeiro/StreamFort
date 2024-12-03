#!/bin/bash

FOLDER=$(pwd)

cd $FOLDER
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

echo "#!/bin/bash" >> pmscript.sh
echo "cd $FOLDER" >> pmscript.sh
echo "source venv/bin/activate" >> pmscript.sh
echo "streamlit run main.py --server.port 8502" >> pmscript.sh
chmod +x pmscript.sh
sudo mv pmscript.sh /usr/bin/

echo "[Unit]" >> pmscript.service
echo "Description=Gerenciador de Senhas" >> pmscript.service
echo "[Service]" >> pmscript.service
echo "ExecStart=/usr/bin/pmscript.sh" >> pmscript.service
echo "[Install]" >> pmscript.service
echo "WantedBy=multi-user.target" >> pmscript.service
sudo mv pmscript.service /lib/systemd/system

sudo systemctl enable pmscript.service
sudo systemctl daemon-reload
sudo systemctl start pmscript.service
