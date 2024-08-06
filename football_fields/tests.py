# misol uchun Reservation(start_time=14:00,end_time=17:00)
# Reservation(start_time=12:00,end_time=13:00)
# Reservation(start_time=11:00,end_time=12:00)
# Reservation(start_time=08:00,end_time=10:00)
#
# obectlar bor , men 17:00 va 18:00  True qaytarish kerak
# 07:00 8:00 kiritganimda ham True qatarishi kerak
#
# 07:00 10:00 kirtiganimda False qaytarishi kerak
# 08:00 10:00 kirtiganimda False qaytarishi kerak
# 16:00 18:00 kirtiganimda False qaytarishi kerak
# 07:00 09:00
# 16:00 18:00
#
# start_time__gte=start_time, end_time__lte=end_time, (Ortaliqdagi hammasini oladi.)
#end_time__gt = start_time , end_time__lte = end_time
# start_time__gte = start_time, start_time__lt = end_time
# Q(start_time__gte=start_time, end_time__lte=end_time) | Q(start_time__lt=start_time, start_time__gt=end_time) | Q(end_time__lt=start_time, end_time__gt=end_time)

# 08:00>07:00
# 08:00>=09:00
#
# 17:00 > 16:00 17:00<=18:00