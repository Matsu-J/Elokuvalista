def check_post_parameters(title, year, hours, minutes, grade):
    error = None
    print(title, year, hours, minutes, grade)

    if len(title) > 30:
        error = "VIRHE: Tarkista nimen pituus"
        return error

    if year != None:
        try:
            year = int(year)
            if year < 0:
                raise ValueError
            if len(str(year)) > 4:
                raise ValueError
        except:
            error = "VIRHE: Tarkista vuosi"
            return error
    
    if hours != None:
        try:
            hours = int(hours)
            if hours < 0:
                raise ValueError
        except:
            error = "VIRHE: Tarkista tunnit"
            return error
    
    if minutes != None:
        try:
            minutes = int(minutes)
            if minutes < 0 or minutes > 60:
                raise ValueError
        except:
            error = "VIRHE: tarkista minuutit"
    
    if grade != None:
        try:
            if "," in grade:
                grade = grade.replace(",",".")
            grade = float(grade)
            if 1 > grade or grade > 10:
                raise ValueError
        except:
            error = "VIRHE: Anna arvosana asteikolla 1-10"
            return error
    
    return error


def check_comment(comment, grade):
    if len(comment) > 200:
        return "Kommentti voi olla korkeintaan 200 merkkiä pitkä"
    
    if grade != None:
        try:
            if "," in grade:
                grade = grade.replace(",",".")
            grade = float(grade)
            if 1 > grade or grade > 10:
                raise ValueError
        except:
            error = "VIRHE: Anna arvosana asteikolla 1-10"
            return error
        
    return None