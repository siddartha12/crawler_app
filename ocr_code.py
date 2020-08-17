import csv,re
with open("phone_dataset.csv","r") as phonebook:
    total_records = csv.reader(phonebook)
    list1 = []
    for each_rec in total_records:
        for det_rec in each_rec:
            list1.append(det_rec)
    list2 = []
    for rec in list1:
        tel_info = rec.split(',')
        for inde in range(0,len(tel_info)):
            tel_info[inde] = tel_info[inde].strip()
            if tel_info[2].isdigit() or any(i.isdigit() for i in tel_info[2]):
                tel_info[2], tel_info[3] = tel_info[3], tel_info[2]
                if tel_info[3].strip().isdigit():
                    tel_info[3] = '(%s) %s-%s' % tuple(re.findall(r'\d{4}$|\d{3}', tel_info[3]))
        list2.append(tel_info)

with open("query.txt","r") as query:
    data_query = query.read()
    query_data = data_query.split('\n')
    count = 0
    with open("output.txt","w") as out:
        for name in query_data:
            for data in list2:
                outval = ' '
                if  name in data:
                    count = count + 1 
                    if count == 1:
                        out1 = "Matches for: "+ name+'\n'
                        out.write(out1)
                    i = 0
                    for each in data:
                        if i == 0:
                            outval += each
                        else:
                            outval += ', '+each
                        i += 1
                    out2 = "Result"+str(count)+':'+outval+'\n'
                    out.write(out2)
            count = 0
        else:
            out3 = "Matches for: "+ name +'\n'
            out.write(out3)
            out.write('No results found')