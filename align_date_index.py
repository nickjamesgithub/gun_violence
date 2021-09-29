import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

data = pd.read_csv("/Users/tassjames/Desktop/Guns/Gun_Violence_01-2013_03-2018.csv")
data["date"] = pd.to_datetime(data["date"]).dt.strftime('%Y-%m-%d')
names = data["state"].unique()
names.sort()

# Date axis
date_index = pd.date_range("2014-01-01", "2018-03-31", freq='D').strftime('%Y-%m-%d')
date_index_array = np.array(date_index)
killed_list = []
incident_list = []
injured_list = []

# Sort new clean cases and deaths lists
for i in range(len(names)):
    # Print name of state
    print(names[i])

    #todo KILLED
    state = data.loc[data['state'] == str(names[i])]
    state_killed = state[['date', 'n_killed']]
    state_killed['date'] = pd.to_datetime(state_killed['date'], errors='coerce') # Make state killed datetime
    data_reg = pd.DataFrame(np.asarray([date_index, np.zeros(len(date_index))]).T, columns=['date', 'zero'])
    data_reg['date'] = pd.to_datetime(data_reg['date'], errors='coerce') # Make dates datetime
    state_new_killed = pd.merge(data_reg, state_killed, on="date", how='left') # Merge on left
    state_new_killed.n_killed[np.isnan(state_new_killed.n_killed)] = 0
    state_new_killed['n_killed'] = state_new_killed.zero + state_new_killed.n_killed # Number killed

    # Update for daily counts of number killed
    state_new_killed['date'] = pd.to_datetime(state_new_killed['date'])
    state_new_killed = state_new_killed.set_index('date')
    daily_summary_killed = state_new_killed.n_killed.resample('D').sum() # Compute daily counts of killed on each day

    # Append n_killed/state each day to list
    killed_list.append(np.array(daily_summary_killed).flatten()) # Killed list

    # todo NUMBER OF INCIDENTS
    state = data.loc[data['state'] == str(names[i])]
    state_incidents = state[['date', 'incident_id']]
    state_incidents['date'] = pd.to_datetime(state_incidents['date'], errors='coerce') # Make state incidents datetime
    # Align with incidents
    data_reg = pd.DataFrame(np.asarray([date_index, np.zeros(len(date_index))]).T, columns=['date', 'zero'])
    data_reg['date'] = pd.to_datetime(data_reg['date'], errors='coerce') # Make dates datetime
    state_incidents = pd.merge(data_reg, state_incidents, on="date", how='left') # Merge on left
    state_incidents.incident_id[np.isnan(state_incidents.incident_id)] = 0
    state_incidents['incident_id'] = state_incidents.zero + state_incidents.incident_id # Number of incidents

    # Update for daily Number of incidents
    state_incidents['date'] = pd.to_datetime(state_incidents['date'])
    state_incidents = state_incidents.set_index('date')
    state_incidents_grid = state_incidents.resample('D').apply({'incident_id': 'count'})
    incident_list.append(np.array(state_incidents_grid.incident_id))

    # state_deaths = state[['date', 'deaths']]
    # state_deaths['date'] = pd.to_datetime(state_deaths['date'], errors='coerce')
    # data_reg = pd.DataFrame(np.asarray([date_index, np.zeros(len(date_index))]).T, columns=['date', 'zero'])
    # # data_reg['date'] = data_reg['date'].dt.strftime('%Y-%m-%d')
    # data_reg['date'] = pd.to_datetime(data_reg['date'], errors='coerce')
    # state_new_deaths = pd.merge(data_reg, state_deaths, on="date", how='left')
    # state_new_deaths.deaths[np.isnan(state_new_deaths.deaths)] = 0
    # state_new_deaths['deaths_new'] = state_new_deaths.zero + state_new_deaths.deaths
    # deaths_list.append(state_new_deaths['deaths_new'])

# Generate cases and deaths matrices
killed_df = pd.DataFrame(killed_list, index=names)
incident_df = pd.DataFrame(incident_list, index=names)

incident_df.to_csv("/Users/tassjames/Desktop/gun_incidents_2014_2018.csv")

# Loop over number killed
for i in range(len(killed_list)):
    plt.plot(killed_list[i])
    plt.title(names[i])
    plt.savefig(names[i]+"_killed")
    plt.show()

    plt.plot(incident_list[i])
    plt.title(names[i])
    plt.savefig(names[i] + "_incidents")
    plt.show()