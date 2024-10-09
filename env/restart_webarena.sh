#!/bin/bash

HOSTNAME=$WEBARENA_HOST

echo "Restarting services on $HOSTNAME..."

ssh -t ubuntu@$HOSTNAME << EOF
  # Function to restart a container if it's running
  restart_container() {
    container_name=\$1
    if [ \$(docker ps -q -f name=\$container_name) ]; then
      echo "Restarting \$container_name..."
      docker restart \$container_name
    else
      echo "\$container_name is not running. Starting it..."
      docker start \$container_name
    fi
  }

  restart_container gitlab
  restart_container shopping
  restart_container shopping_admin
  restart_container forum
  restart_container kiwix33

  cd /home/ubuntu/openstreetmap-website/
  docker compose restart

  echo "Updating Magento configuration..."
  docker exec shopping /var/www/magento2/bin/magento setup:store-config:set --base-url="http://$HOSTNAME:7770"
  docker exec shopping mysql -u magentouser -pMyPassword magentodb -e "UPDATE core_config_data SET value='http://$HOSTNAME:7770/' WHERE path = 'web/secure/base_url';"

  docker exec shopping_admin php /var/www/magento2/bin/magento config:set admin/security/password_is_forced 0
  docker exec shopping_admin php /var/www/magento2/bin/magento config:set admin/security/password_lifetime 0
  docker exec shopping /var/www/magento2/bin/magento cache:flush

  docker exec shopping_admin /var/www/magento2/bin/magento setup:store-config:set --base-url="http://$HOSTNAME:7780"
  docker exec shopping_admin mysql -u magentouser -pMyPassword magentodb -e "UPDATE core_config_data SET value='http://$HOSTNAME:7780/' WHERE path = 'web/secure/base_url';"
  docker exec shopping_admin /var/www/magento2/bin/magento cache:flush

  echo "Reconfiguring GitLab..."
  docker exec gitlab sed -i "s|^external_url.*|external_url 'http://$HOSTNAME:8023'|" /etc/gitlab/gitlab.rb
  docker exec gitlab gitlab-ctl reconfigure
EOF

echo "Services have been restarted successfully."

echo export SHOPPING="http://$HOSTNAME:7770"
echo export SHOPPING_ADMIN="http://$HOSTNAME:7780/admin"
echo export REDDIT="http://$HOSTNAME:9999"
echo export GITLAB="http://$HOSTNAME:8023"
echo export MAP="http://$HOSTNAME:3000"
echo export WIKIPEDIA="http://$HOSTNAME:8888/wikipedia_en_all_maxi_2022-05/A/User:The_other_Kiwix_guy/Landing"
echo export HOMEPAGE="http://$HOSTNAME:4399"
