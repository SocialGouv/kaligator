# you can run this in another terminal to follow the progress
# of convert_xml_to_json.py script.

count=`ls converted_jsons|wc -l`
total=191061
start=`date +%s`

while [ $count -lt $total ]; do
  sleep 2 # this is work
  cur=`date +%s`
  count=`ls converted_jsons|wc -l`
  pd=$(( $count * 73 / $total ))
  runtime=$(( $cur-$start ))
  estremain=$(( ($runtime * $total / $count)-$runtime ))
  printf "\r%d.%d%% complete ($count of $total) - est %d:%0.2d remaining\e[K" $(( $count*100/$total )) $(( ($count*1000/$total)%10)) $(( $estremain/60 )) $(( $estremain%60 ))
done
printf "\ndone\n"
