import csvlib
import datetimes as d


def parsing(time):
    return d.timedelta(hours=int(time.split(":")[0]), minutes=int(time.split(":")[1]), seconds=int(time.split(":")[2]))

def parsing_date(day):
    return d.date(int(day.split("-")[0]),int(day.split("-")[1]),int(day.split("-")[2]))
def if_week(day):
    if d.datetime.strptime(day, format).isoweekday() > 5:
        return True
    else:
        return False
def timedelta_to_hours(hours):
    return str(int(hours.total_seconds()//3600))+":"+str(int((hours.total_seconds()-(hours.total_seconds()//3600)*3600)//60))+":"+str(int(hours.total_seconds()%60))
def parsing_overtime(o_hours):
    if o_hours.total_seconds()>0:
        return str(o_hours)
    else:
        return str("-"+str(abs(o_hours)))

work_entries = []#work_entries contain all entries about employee
only_date = []#contain only dates
entrances = ['E/0/KD1/7-9', 'E/0/KD1/7-8', 'E/0/KD1/8-8']#entrance to the building
with open('input.csv') as csvfile:#reading csv file and write these datas
    worker = csvlib.reader(csvfile, delimiter=';')
    for row in worker:
        work_entries.append(row)
        only_date.append(row[0].split()[0])
try:
    work_entries.remove(['Date', 'Event', 'Gate'])
except:
    pass
try:
    only_date.remove('Date')
except:
    pass
WORKDAY=parsing('8:00:00')
day_in_week=parsing_date(only_date[0])
start_week = day_in_week - d.timedelta(days=day_in_week.weekday())
end_week = start_week + d.timedelta(days=6)
hours_in_building = []
last=False
hours_at_week_work=parsing('00:00:00')
overtime_hours=parsing('00:00:00')
uniq_dates = sorted(list(set(only_date)))
format="%Y-%m-%d"
#main loop to iterate through uniq dates
for j in range(len(uniq_dates)):
    searchval = uniq_dates[j]
    if parsing_date(searchval)>end_week:#counting hours in week and overtime
        hours_in_building.append(timedelta_to_hours(hours_at_week_work))
        hours_in_building.append(parsing_overtime(overtime_hours))
        hours_at_week_work = parsing('00:00:00')
        overtime_hours = parsing('00:00:00')
        start_week = parsing_date(searchval) - d.timedelta(days=day_in_week.weekday())
        end_week = start_week + d.timedelta(days=6)
    index_of_searchvalues = [i for i, val in enumerate(only_date) if val == searchval]#finding all index of date
    if work_entries[index_of_searchvalues[-1]][1] == "Reader exit" and work_entries[index_of_searchvalues[-1]][2].strip() in entrances:#finding if last date have reader exit and employee went out from building
        start_hour = parsing(work_entries[index_of_searchvalues[0]][0].split()[1])
        hours_at_day_work = parsing('00:00:00')
        for k in index_of_searchvalues[1:]:
            if k == index_of_searchvalues[-1]:#if responding for last entry on day
                start_hour = parsing(work_entries[k][0].split()[1])
                hours_at_day_work += start_hour - end_hour
                if j==(len(uniq_dates) - 1):#if it is last date and last entry in file last=true
                    last=True

            else:
                if work_entries[k][1] == "Reader exit" and work_entries[k][2].strip() in entrances:
                    end_hour = parsing(work_entries[k][0].split()[1])
                    hours_at_day_work += (end_hour - start_hour)
                    start_hour=parsing(work_entries[k + 1][0].split()[1])
                else:
                    end_hour = parsing(work_entries[k][0].split()[1])
                    hours_at_day_work += (end_hour - start_hour)
                    start_hour = end_hour
        if if_week(work_entries[k][0].split()[0]):
            if hours_at_day_work.seconds // 3600 >= 9:
                hours_in_building.append("Day " + work_entries[k][0].split()[0] + " Work " + str(hours_at_day_work) + " w ot")
                hours_at_week_work+=hours_at_day_work
                overtime_hours+=(hours_at_day_work-WORKDAY)
            elif hours_at_day_work.seconds // 3600 < 6:
                hours_in_building.append("Day " + work_entries[k][0].split()[0] + " Work " + str(hours_at_day_work) + " w ut")
                hours_at_week_work += hours_at_day_work
                overtime_hours += (hours_at_day_work-WORKDAY)
            else:
                hours_in_building.append("Day " + work_entries[k][0].split()[0] + " Work " + str(hours_at_day_work) + " w")
                hours_at_week_work += hours_at_day_work
                overtime_hours += (hours_at_day_work-WORKDAY)
        else:
            if hours_at_day_work.seconds // 3600 >= 9:
                hours_in_building.append("Day " + work_entries[k][0].split()[0] + " Work " + str(hours_at_day_work) + " ot")
                hours_at_week_work += hours_at_day_work
                overtime_hours += (hours_at_day_work-WORKDAY)
            elif hours_at_day_work.seconds // 3600 < 6:
                hours_in_building.append("Day " + work_entries[k][0].split()[0] + " Work " + str(hours_at_day_work) + " ut")
                hours_at_week_work += hours_at_day_work
                overtime_hours += (hours_at_day_work-WORKDAY)
            else:
                hours_in_building.append("Day " + work_entries[k][0].split()[0] + " Work " + str(hours_at_day_work))
                hours_at_week_work += hours_at_day_work
                overtime_hours += (hours_at_day_work-WORKDAY )

    else:
        last_entries_in_day=work_entries[index_of_searchvalues[-1]][0].split()
        hours_at_day_work = parsing(last_entries_in_day[1]) - parsing(work_entries[k + 1][0].split()[1])
        if if_week(last_entries_in_day[0]):
            hours_in_building.append("Day " + last_entries_in_day[0] + " Work " + str(hours_at_day_work) + " w i")
            hours_at_week_work += hours_at_day_work
            overtime_hours += (hours_at_day_work-WORKDAY)
        else:
            hours_in_building.append("Day " + last_entries_in_day[0] + " Work " + str(hours_at_day_work) + " i")
            hours_at_week_work += hours_at_day_work
            overtime_hours += (hours_at_day_work-WORKDAY)
    if last:
        hours_in_building.append(timedelta_to_hours(hours_at_week_work))
        hours_in_building.append(parsing_overtime(overtime_hours))

with open('result', 'w') as f:
    for item in hours_in_building:
        f.write("%s\n" % item)
