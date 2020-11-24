#!/bin/sh

num_tests=(0 7 100 1025 133562368)

# Test 1: basic case (./randall NUMBYTES)
for N in "${num_tests[@]}";
do
  if [ "$(./randall "$N" | wc -c)" = "$N" ]
  then
    echo "test passed -> ./randall $N"
  else
    echo "test failed -> ./randall $N"
  fi
done

# Test 2: ./randall NUMBYTES -i rdrand
for N in "${num_tests[@]}";
do
  I="rdrand"
  if [ "$(./randall "$N" -i "$I" | wc -c)" = "$N" ]
  then
    echo "test passed -> ./randall $N -i $I"
  else
    echo "test failed -> ./randall $N -i $I"
  fi
done

# Test 3: ./randall NUMBYTES -i mrand48_r
for N in "${num_tests[@]}";
do
  I="mrand48_r"
  if [ "$(./randall "$N" -i "$I" | wc -c)" = "$N" ]
  then
    echo "test passed -> ./randall $N -i $I"
  else
    echo "test failed -> ./randall $N -i $I"
  fi
done

# Test 4: ./randall NUMBYTES -i /dev/urandom
for N in "${num_tests[@]}";
do
  I="/dev/urandom"
  if [ "$(./randall "$N" -i "$I" | wc -c)" = "$N" ]
  then
    echo "test passed -> ./randall $N -i $I"
  else
    echo "test failed -> ./randall $N -i $I"
  fi
done

# Test 5: ./randall NUMBYTES -o stdio
for N in "${num_tests[@]}";
do
  O="stdio"
  if [ "$(./randall "$N" -o "$O" | wc -c)" = "$N" ]
  then
    echo "test passed -> ./randall $N -o $O"
  else
    echo "test failed -> ./randall $N -o $O"
  fi
done

# Test 6: ./randall NUMBYTES -o 1
for N in "${num_tests[@]}";
do
  O="1"
  if [ "$(./randall "$N" -o "$O" | wc -c)" = "$N" ]
  then
    echo "test passed -> ./randall $N -o $O"
  else
    echo "test failed -> ./randall $N -o $O"
  fi
done

# Test 7: ./randall NUMBYTES -i mrand48_r -o 1
for N in "${num_tests[@]}";
do
  I="mrand48_r"
  O="1"
  if [ "$(./randall "$N" -i "$I" -o "$O" | wc -c)" = "$N" ]
  then
    echo "test passed -> ./randall $N -i $I -o $O"
  else
    echo "test failed -> ./randall $N -i $I -o $O"
  fi
done

# Test 8: ./randall -i rdrand NUMBYTES -o 2
for N in "${num_tests[@]}";
do
  I="rdrand"
  O="2"
  if [ "$(./randall -i "$I" "$N" -o "$O" | wc -c)" = "$N" ]
  then
    echo "test passed -> ./randall -i $I $N -o $O"
  else
    echo "test failed -> ./randall -i $I $N -o $O"
  fi
done

# Test 9: ./randall -i /dev/urandom -o stdio NUMBYTES
for N in "${num_tests[@]}";
do
  I="/dev/urandom"
  O="stdio"
  if [ "$(./randall -i "$I" -o "$O" "$N" | wc -c)" = "$N" ]
  then
    echo "test passed -> ./randall -i $I -o $O $N"
  else
    echo "test failed -> ./randall -i $I -o $O $N"
  fi
done

