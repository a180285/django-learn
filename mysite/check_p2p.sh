while [[ 1 ]]; do
  ./manage.py check_p2p
  echo ""
  echo "sleep ..."
  sleep 300
done

