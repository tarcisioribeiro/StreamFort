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

title() {
    echo -e "$(toilet --font pagga --filter border --width 120 "$1")"
}

FOLDER=$(pwd)
actual_date=$(date +"%Y-%m-%d")
actual_horary=$(date +"%H_%M_%S")
database_backup_filename="backup_seguranca_${actual_date}_${actual_horary}.sql"
backup_directory_name="streamfort_data_backup_${actual_date}_${actual_horary}"

echo ""
title "Desinstalação do StreamFort"

while true; do
    blue "\nDigite a senha de root:"
    read -s root_password
    sleep 1
    echo "$root_password" | sudo -S echo "Senha de root aceita."

    if [ $? -eq 0 ]; then
        green "\nVocê tem permissões de root. Continuando com o script..."
        sleep 1
        blue "\nDesativando o serviço da aplicação..."
        sleep 1
        sudo systemctl stop streamfort.service
        sudo systemctl disable streamfort.service
        sudo rm /lib/systemd/system/streamfort.service
        sudo rm /usr/bin/streamfort.sh
        break
    else
        red "\nSenha de root incorreta. Saindo..."
        sleep 1
        exit 1
    fi
done

sleep 1

while true; do
    blue "\nDigite a senha do banco de dados: "
    read -s password
    sleep 1
    blue "\nRepita a senha: "
    read -s confirmation
    sleep 1

    if [ "$password" = "$confirmation" ]; then
        green "\nSenhas coincidem. Realizando o backup do banco de dados..."
        sleep 1
        mysqldump -uroot -p"$password" --databases seguranca > "$database_backup_filename"
        chmod 700 "$database_backup_filename"
        red "\nApagando a base de dados...\n"
        sleep 1
        mysql -uroot -p"$password" -e "DROP DATABASE seguranca;" 2>/dev/null
        if [ $? -eq 0 ]; then
            green "\nBase de dados apagada com sucesso."
        else
            red "\nFalha ao apagar a base de dados. Verifique se a base de dados existe."
        fi
        break
    else
        red "\nAs senhas não coincidem. Tente novamente."
        sleep 1
    fi
done

cd $FOLDER
mkdir "$backup_directory_name"
mv "$database_backup_filename" "$backup_directory_name"
green "\nO backup da base de dados foi salvo no diretório '$FOLDER/$backup_directory_name'."

sleep 1

blue "\nDesativando ambiente virtual..."
sleep 1
blue "\nRemovendo ambiente virtual..."
sleep 1
rm -rf venv

sleep 1

green "\nDesinstalação concluída."
