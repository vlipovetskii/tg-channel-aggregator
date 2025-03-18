function ok_exit_w {

	read -rp "OK. Press [Enter] key to exit. Or Ctrl-C to stay in terminal."
	exit

}

function error_exit_w {

	# echo "errno=$1"

	read -rp "Error. Press [Enter] key to exit. Or Ctrl-C to stay in terminal."
	exit

}
