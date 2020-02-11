import firebase_admin
from firebase_admin import credentials, db
from datetime import datetime, timedelta
import matplotlib
matplotlib.use('PS')
import matplotlib.pyplot as plt
from matplotlib.dates import DayLocator, DateFormatter


cred = credentials.Certificate('key.json')
firebase_admin.initialize_app(cred, {
    'databaseURL' : 'https://post-visualize.firebaseio.com/'
})

#Gets data and organizes it by plant from firebase. Returns a Dictionary
#holding the data
def get_graph_data():
    ref = db.reference()
    data = ref.get()
    key_array = []
    for key in data:
        key_array.append(key)
    plant_data_dict = {}
    for key in key_array:
        curr_record = data[key]
        curr_data = curr_record['data'][0]
        plant = 0
        if 'plant' in curr_data and curr_data['plant'] != 'test':
            plant = curr_data['plant']
        else:
            continue
        if plant not in plant_data_dict:
            plant_data_dict[plant] = [curr_data]
        else:
            updated_data = plant_data_dict[plant]
            updated_data.append(curr_data)
            plant_data_dict[plant] = updated_data
    return plant_data_dict

def create_graph(plant_name, data_dict):
    relevant_data = data_dict[plant_name]
    date_to_data= {}
    for data_point in relevant_data:
        date = data_point['timeFinished']
        t_index = date.index("T")
        final_date = date[:t_index]
        final_time = date[t_index + 1: -1]
        final_total_date = final_date + " " + final_time
        datetime_object = datetime.strptime(final_total_date, '%Y-%m-%d %H:%M:%S.%f')
        if 'rawWaterTurbidity' not in data_point or 'filteredWaterTurbidity1' not in data_point or "settledWaterTurbidity" not in data_point or 'coagulantDose' not in data_point:
            continue
        else:
            raw_data = data_point['rawWaterTurbidity']
            filtered_data = data_point['filteredWaterTurbidity1']
            settled_data = data_point["settledWaterTurbidity"]
            coagulant_data = data_point['coagulantDose']
            date_to_data[datetime_object] = [raw_data, filtered_data, settled_data, coagulant_data]
    date_list = []
    i = 30;
    date_end = datetime.now()
    date_start = datetime.now() - timedelta(days=30)
    for key in date_to_data.keys():
        if date_start <= key <= date_end:
            lst = date_to_data[key]
            date_list.append((key, lst))
    raw_water_y = []
    filtered_water_y = []
    settled_water_y = []
    coagulant_y = []
    final_date_lst = []
    result = sorted(date_list, key=lambda x: x[0])
    for res in result:
        raw_water_y.append(res[1][0])
        filtered_water_y.append(res[1][1])
        settled_water_y.append(res[1][2])
        coagulant_y.append(res[1][3])
        final_date_lst.append(res[0])






    plt.figure(0)
    plt.gca().xaxis.set_major_formatter(matplotlib.dates.DateFormatter('%m/%d/%Y'))
    plt.gca().xaxis.set_major_locator(DayLocator(interval=5))
    plt.gca().tick_params(axis = 'both', which = 'major', labelsize = 5)
    plt.plot(final_date_lst,raw_water_y)
    plt.plot(final_date_lst,filtered_water_y)
    plt.plot(final_date_lst,settled_water_y)
    plt.legend(['Cruda', 'Decantada', 'Filtrada'], loc='upper right')
    plt.ylabel("Turbiedad (UTN)")
    plt.title(plant_name)
    for_title = datetime.now()
    for_title = for_title.strftime('%m:%d:%Y')
    plt.savefig(plant_name + for_title + '1.jpg', dpi=500)


    plt.figure(1)
    plt.gca().xaxis.set_major_formatter(matplotlib.dates.DateFormatter('%m/%d/%Y'))
    plt.gca().xaxis.set_major_locator(DayLocator(interval=5))
    plt.gca().tick_params(axis = 'both', which = 'major', labelsize = 5)
    plt.plot(final_date_lst,coagulant_y)
    plt.ylabel("mg/L")
    plt.title("Dosis De Coagulantes")
    plt.savefig(plant_name + for_title + '2.jpg', dpi=500)

    data_submitted = len(date_list)
    if data_submitted > 50:
        return "good"
    if data_submitted >= 25 and data_submitted <= 50:
        return "ok"
    if data_submitted < 25:
        return "bad"

if __name__=="__main__":
    data = get_graph_data()
    lst = {}
    for plant in data:
        plant_data = data[plant]
        for data_point in plant_data:
            date = data_point['timeFinished']
            t_index = date.index("T")
            final_date = date[:t_index]
            final_time = date[t_index + 1: -1]
            final_total_date = final_date + " " + final_time
            datetime_object = datetime.strptime(final_total_date, '%Y-%m-%d %H:%M:%S.%f')
            print(datetime_object)
