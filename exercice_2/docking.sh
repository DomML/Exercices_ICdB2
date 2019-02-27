#!/bin/bash -i

###Converted from AttractEasyModel by easy2model 1.1
### Generated by ATTRACT shell script generator version 0.5

set -u -e
trap "kill -- -$BASHPID; $ATTRACTDIR/shm-clean" ERR EXIT
$ATTRACTDIR/shm-clean

rm -rf result.dat result.pdb result.lrmsd result.irmsd result.fnat >& /dev/null

#name of the run
name=attract_2018_04_17

#docking parameters
params="$ATTRACTDIR/../attract.par receptorr.pdb ligandr.pdb --fix-receptor"
scoreparams="$ATTRACTDIR/../attract.par receptorr.pdb ligandr.pdb --score --fix-receptor"

#grid parameters
gridparams=" --grid 1 receptorgrid.gridheader"

#parallelization parameters
parals="--np 8 --chunks 8"
if [ 1 -eq 1 ]; then ### move and change to disable parts of the protocol

echo '**************************************************************'
echo 'Reduce partner PDBs...'
echo '**************************************************************'
python $ATTRACTTOOLS/reduce.py receptor.pdb receptorr.pdb --chain A > /dev/null
python $ATTRACTTOOLS/reduce.py ligand.pdb ligandr.pdb --rna --chain B > /dev/null

echo '**************************************************************'
echo 'Generate starting structures...'
echo '**************************************************************'
cat $ATTRACTDIR/../rotation.dat > rotation.dat
$ATTRACTDIR/translate receptorr.pdb ligandr.pdb > translate.dat
$ATTRACTDIR/systsearch > systsearch.dat
start=systsearch.dat

echo '**************************************************************'
echo 'calculate receptorgrid grid'
echo '**************************************************************'
awk '{print substr($0,58,2)}' ligandr.pdb | sort -nu > receptorgrid.alphabet
$ATTRACTDIR/make-grid-omp receptorr.pdb $ATTRACTDIR/../attract.par 5.0 7.0 receptorgrid.gridheader  --shm --alphabet receptorgrid.alphabet

echo '**************************************************************'
echo 'Docking'
echo '**************************************************************'

echo '**************************************************************'
echo '1st minimization'
echo '**************************************************************'
python $ATTRACTDIR/../protocols/attract.py $start $params $gridparams --vmax 1000 $parals --output out_$name.dat

echo '**************************************************************'
echo 'Final rescoring'
echo '**************************************************************'
python $ATTRACTDIR/../protocols/attract.py out_$name.dat $scoreparams --rcut 50.0 $parals --output out_$name.score

echo '**************************************************************'
echo 'Merge the scores with the structures'
echo '**************************************************************'
python $ATTRACTTOOLS/fill-energies.py out_$name.dat out_$name.score > out_$name-scored.dat

echo '**************************************************************'
echo 'Sort structures'
echo '**************************************************************'
python $ATTRACTTOOLS/sort.py out_$name-scored.dat > out_$name-sorted.dat

echo '**************************************************************'
echo 'Remove redundant structures'
echo '**************************************************************'
$ATTRACTDIR/deredundant out_$name-sorted.dat 2 | python $ATTRACTTOOLS/fill-deredundant.py /dev/stdin out_$name-sorted.dat > out_$name-sorted-dr.dat

echo '**************************************************************'
echo 'Soft-link the final results'
echo '**************************************************************'
ln -s out_$name-sorted-dr.dat result.dat

echo '**************************************************************'
echo 'collect top 50 structures:'
echo '**************************************************************'
$ATTRACTTOOLS/top out_$name-sorted-dr.dat 50 > out_$name-top50.dat
$ATTRACTDIR/collect out_$name-top50.dat receptor-aa.pdb ligand-aa.pdb > out_$name-top50.pdb
ln -s out_$name-top50.pdb result.pdb

$ATTRACTDIR/shm-clean

fi ### move to disable parts of the protocol