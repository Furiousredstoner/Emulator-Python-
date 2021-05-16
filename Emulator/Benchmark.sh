python3 -m pip install --upgrade pip
python3 -m pip install snakeviz
python3 -m cProfile -o benchmark.prof main.py
snakeviz benchmark.prof
