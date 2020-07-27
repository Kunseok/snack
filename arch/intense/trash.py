
for dt in range(1,32):
    d = dt
    if d < 10:
        d ="0"+str(d)
    for mo in range(1,13):
        m = mo
        if m < 10:
            m ="0"+str(m)

        print("2020-"+str(m)+"-"+str(d))
