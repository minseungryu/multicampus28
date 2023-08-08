import pandas as pd

def main():
    data = pd.read_json("population.json")
    data = pd.DataFrame(data)

    print(data.head())

if __name__ == "__main__":
    main()