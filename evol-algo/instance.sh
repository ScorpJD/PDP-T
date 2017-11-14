# rm -r Instance
mkdir Instance
cd Instance
wget https://www.sintef.no/contentassets/1338af68996841d3922bc8e87adc430c/pdp_100.zip
unzip pdp_100.zip
mv pdp_100/ data/
rm pdp_100.zip
find data | grep -v "lrcc*" | xargs rm

mkdir sol
cd sol
for i in $(seq 1 8)
do
    for j in 10 20
    do
        wget https://www.sintef.no/contentassets/abb42d6b3f82453cb1908ed546b24fca/lrc$j$i.txt
    done
done
