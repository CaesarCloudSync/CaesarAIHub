if [[ $1 == "" ]]
then
  python -m unittest caesaraiunit.CaesarAIUnittest
else
  python -m unittest caesaraiunit.CaesarAIUnittest.$1
fi