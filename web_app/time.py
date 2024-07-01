import datetime as dt
start="09:15:00"
end="10:15:00"
slot=4
start_dt = dt.datetime.strptime(start, '%H:%M:%S')
end_dt = dt.datetime.strptime(end, '%H:%M:%S')
diff = (end_dt - start_dt)

print(diff)

diff_in_min = diff * 60
print(diff_in_min)




import datetime as dt
class TimeSlots():
  @staticmethod
  def time_slots(start, end, duration):
    start_time = dt.datetime.strptime(start, '%H:%M')
    end_time = dt.datetime.strptime(end, '%H:%M')
    time_interval = dt.datetime.strptime(duration, '%M')
    time_zero = dt.datetime.strptime('00:00', '%H:%M')
    timeslots = []
    while end_time > start_time:
      end = ((start_time - time_zero + time_interval))
      timeslot = f'{(start_time).time() }'
      h, m, s = timeslot.split(":")
      timeslots.append('{0}:{1}'.format(h,m))
      start_time = end
    return timeslots
print(TimeSlots.time_slots("15:00", "18:00", "20"))