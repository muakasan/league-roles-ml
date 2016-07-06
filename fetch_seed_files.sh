for i in `seq 1 10`;
do 
	wget "https://s3-us-west-1.amazonaws.com/riot-api/seed_data/matches"$i".json" -P seed-files/
done
 
