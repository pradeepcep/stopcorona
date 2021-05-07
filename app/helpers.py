def normalise_institution_name(institution_name, max_length=500):
    '''
    Normalise the institution name so that we can use it as a unique reference.
    '''
    return institution_name.strip().lower(). \
        replace(', ', '-'). \
        replace('. ', '-'). \
        replace(' ', '-'). \
        replace('.', '-'). \
        replace(',', '-'). \
        replace("'", '-')
