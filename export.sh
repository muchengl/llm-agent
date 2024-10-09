source ./aws/aws-cli.sh
export WEBARENA_HOST=$(get_ec2_dns "WebArenaEc2Stack/WebArenaServer")
echo "WebArena Host: $WEBARENA_HOST"

HOSTNAME=$WEBARENA_HOST

echo export WEBARENA_HOST=$WEBARENA_HOST
echo export SHOPPING="http://$HOSTNAME:7770"
echo export SHOPPING_ADMIN="http://$HOSTNAME:7780/admin"
echo export REDDIT="http://$HOSTNAME:9999"
echo export GITLAB="http://$HOSTNAME:8023"
echo export MAP="http://$HOSTNAME:3000"
echo export WIKIPEDIA="http://$HOSTNAME:8888/wikipedia_en_all_maxi_2022-05/A/User:The_other_Kiwix_guy/Landing"
echo export HOMEPAGE="http://$HOSTNAME:4399"