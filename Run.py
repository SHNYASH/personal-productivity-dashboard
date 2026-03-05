from Extract import get_events
from Transform import pandas_clean
from Load import load_to_postgres


if __name__ == '__main__':
    #EXTRACT
    raw_data = get_events()
    #TRANSFORM
    if raw_data:
        cleaned_data = pandas_clean(raw_data)
        #LOAD
        load_to_postgres(cleaned_data)
