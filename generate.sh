DIR="ChristmasCarol"

for file in `ls ${DIR}`
do
   `python app.py --in_pic ChristmasCarol/${file} -o dist/`
done
