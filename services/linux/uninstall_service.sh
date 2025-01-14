#!/bin/bash

red() {
    echo -e "\033[31m$1\033[0m"
}
green() {
    echo -e "\033[32m$1\033[0m"
}

blue() {
    echo -e "\033[34m$1\033[0m"
}

actual_date=$(date +"%Y-%m-%d")
actual_horary=$(date +"%H_%M_%S")
database_backup_filename="backup_seguranca_${actual_date}_${actual_horary}.sql"
backup_directory_name="streamfort_data_backup_${actual_date}_${actual_horary}"
FOLDER=$(pwd)

while true; do
    blue "\nDigite a senha de root:"
    read -s root_password
    sleep 5
    blue "\nDigite a senha de root novamente: "
    read -s confirm_root_password
    sleep 5

    echo "$root_password" | sudo -S echo "Senha de root aceita."

    if [ $? -eq 0 ]; then
        green "\nVocê tem permissões de root. Continuando com o script..."
        sleep 5
        blue "\nDesativando o serviço da aplicação..."
        sleep 5
        sudo systemctl stop streamfort.service
        sudo systemctl disable streamfort.service
        sudo rm /lib/systemd/system/streamfort.service
        sudo rm /usr/bin/streamfort.sh
        break
    else
        red "\nSenha de root incorreta. Saindo..."
        sleep 5
        exit 1
    fi
done

sleep 5

while true; do
    blue "\nDigte a senha do banco de dados: "
    read -s password
    sleep 5
    blue "\nRepita a senha: "
    read -s confirmation
    sleep 5

    if [ "$password" = "$confirmation" ]; then
        green "\nSenhas coincidem. Realizando o backup do banco de dados..."
        sleep 3
        mysqldump -uroot -p"$password" --databases seguranca >> $database_backup_filename
        chmod 700 $database_backup_filename
        red "\nApagando a base de dados...\n"
        sleep 3
        mysql -uroot -p"$password" -e "DROP DATABASE seguranca;"
        break
    else
        red "\nAs senhas não coincidem. Tente novamente."
        sleep 5
    fi
done

mkdir "$backup_directory_name"
mv "$database_backup_filename" "$backup_directory_name"
mv "accounts/" "$backup_directory_name"
mv "$backup_directory_name" $HOME
green "\nO backup da base de dados foi salvo no diretório '$HOME/$backup_directory_name'."

sleep 5

blue "\nDesativando ambiente virtual..."
sleep 5
blue "\nRemovendo ambiente virtual..."
sleep 5
rm -r venv

sleep 5

green "\nDesinstalação concluída."
