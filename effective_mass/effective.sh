#!/bin/bash
pat=$(pwd)
file=$pat/BAND_STATS.out
#echo $pat

#!/bin/bash

echo 211 | vaspkit > $file

NKPTS=$(head -2 BAND.dat | tail -1 | awk '{print $5}')
HUMO=$(head -7 BAND_GAP | tail -1 | awk '{print $5}')
LUMO=$(head -7 BAND_GAP | tail -1 | awk '{print $6}')


grep -E "# Band-Index [[:space:]]*$HUMO" -A $NKPTS BAND.dat > vbm.dat
grep -E "# Band-Index [[:space:]]*$LUMO" -A $NKPTS BAND.dat > cbm.dat

#echo "$folder"
#echo "vbm"
python $pat/effective_mass/calculator_effective_mass.py vbm vbm.dat vbm_eff.dat
#echo "cbm"
python $pat/effective_mass/calculator_effective_mass.py cbm cbm.dat cbm_eff.dat

vbm_content=$(head -1 vbm_eff.dat)
cbm_content=$(head -1 cbm_eff.dat)
rm vbm_eff.dat cbm_eff.dat
#echo $vbm_content
#echo $cbm_content

#read -r vbm_index vbm_eff_1 vbm_eff_2 <<< "$vbm_content"
#read -r cbm_index cbm_eff_1 cbm_eff_2 <<< "$cbm_content"

#echo "$strain\t$vbm_index\t$vbm_eff_1\t$vbm_eff_2\t$cbm_index\t$cbm_eff_1\t$cbm_eff_2" >> $file


echo "vbm_index\teff_vbm_1\teff_vbm_2\tcbm_index\teff_cbm_1\teff_cbm_2" > $file

echo "$folder\t$vbm_content\t$cbm_content" >> $file
echo "VBM_DATA\t$vbm_content\nCBM_DATA\t$cbm_content"

