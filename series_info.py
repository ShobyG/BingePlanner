from wiki import find_id, find_season_episodes
import isodate
from datetime import datetime, timedelta
import numpy

class SeriesInfo:
    def __init__(self, imdb_id):
        # print("call SeriesInfo with show id")
        self.series_imdb_id = imdb_id
        # print(self.series_imdb_id)
        # print("call Title api, get series info")
        self.series_info = find_id(self.series_imdb_id)
        # print(self.series_info)
        # print("get array of number of seasons")
        self.seasons_list = self.series_info['tvSeriesInfo']['seasons']
        # print(self.seasons_list)
        self.seasons_tot = len(self.seasons_list)
        # print(self.seasons_tot)
        # print("get title, rating, plot, image")
        self.series_title = self.series_info['title']
        self.series_rating = self.series_info['imDbRating']
        self.series_plot = self.series_info['plot']
        self.series_image = self.series_info['image']
        # print(self.series_title)
        # print(self.series_rating)
        # print(self.series_plot)        
        # print("create empty array of length number of seasons + 1 (for runtime data) (will add rows in series loop)")
        self.series_runtime_data = ['0'] * (self.seasons_tot + 1)
        # print(self.series_runtime_data) 
        # print("create empty array of length number of seasons + 1 (for total season runtime)")
        self.series_runtime_totals = ['0'] * (self.seasons_tot + 1)
        # print("create empty array of length number of seasons + 1 (for season data)")
        self.season_info = ['0'] * (self.seasons_tot + 1)
        # print(self.season_info)
        # print("create empty array of length number of seasons + 1 (for total season episodes)")
        self.season_tot_episodes = ['0'] * (self.seasons_tot + 1)
        # print(self.season_tot_episodes)
        # print("create empty array of length number of seasons + 1 (for season episodes)")
        self.season_episodes = ['0'] * (self.seasons_tot + 1)
        self.__set_series_data()

    def __set_series_data(self):
        # print("for each season in array:")
        self.series_dict = {}
        self.episode_dict = {}
        for i in range(1, len(self.series_runtime_data)):
            # print(f"Season: {i}")
            # print("get season_data from SeasonEpisodes api")
            self.season_info[i] = find_season_episodes(self.series_imdb_id, i)
            # print(self.season_info[i])
            # print("check if episodes")
            self.season_episodes[i] = self.season_info[i]["episodes"]
            # print(self.season_info[i]["episodes"])
            if self.season_info[i]["episodes"] is None:
                break
            # print("get number of episodes from len(season_data['episodes'])")
            self.season_tot_episodes[i] = len(self.season_info[i]["episodes"])
            # print(self.season_tot_episodes[i])
            # print("in runtime_array, create list at element [i] of nulls to hold episode runtimes")
            self.series_runtime_data[int(i)] = [None] * (self.season_tot_episodes[i] + 1)
            # print("for each episode:")
            for j in range(1, self.season_tot_episodes[i] + 1):
                # print(f"Episode: {j}")
                # print("get imdb id for this episode")
                ep_imdb_id = self.season_info[i]['episodes'][j-1]['id']
                # print(ep_imdb_id)
                # print("get all this episode info")
                ep_info = find_id(ep_imdb_id)
                # print(ep_info)
                # print("save episode title, plot, season, number")
                ep_title = ep_info['title']
                ep_plot = ep_info['plot']
                # print(ep_title)
                # print(ep_plot)
                try:
                    ep_season = ep_info['tvEpisodeInfo']['seasonNumber']
                    ep_number = ep_info['tvEpisodeInfo']['episodeNumber']
                    # print(ep_season)
                    # print(ep_number)
                    if ep_season is None:
                        break
                except Exception as e:
                    print(Exception)
                    break
                try:
                    # print("see if there is any runtime info in Title Api for this episode id")
                    ep_run_time = ep_info['runtimeMins']
                    # print(ep_run_time)
                    if ep_run_time is None:
                        break
                except Exception as e:
                    print(Exception)
                    break
                # print("parse letters from runtime string if necessary")
                if ep_run_time[0] == "P":
                    ep_run_time = int(isodate.parse_duration(ep_run_time).total_seconds() / 60)
                else:
                    ep_run_time = int(ep_run_time)
                # print(f"save runtime at runtime_data[{i}][{j}]")
                self.series_runtime_data[int(i)][int(j)] = ep_run_time
                # print(self.series_runtime_data[int(i)][int(j)])
                self.series_runtime_totals[int(i)] = int(self.series_runtime_totals[int(i)])
                self.series_runtime_totals[int(i)] += int(ep_run_time)
                # print(f"print accumulated runtime for season {ep_season}: {self.series_runtime_totals[int(i)]}")
                addlist = [ep_season, ep_number, ep_title, ep_plot, ep_run_time, ep_info]
                # print(f"adding to episode_dict: {addlist}")
                self.add_values(self.episode_dict, ep_imdb_id, addlist)
               
        # print("print episode_dict")
        # print(self.episode_dict)
        # print("print the array of episode runtimes")
        # print(self.series_runtime_data)
        addlist = [self.series_title, self.series_rating, self.series_plot, self.series_image, 
                                            self.seasons_tot, self.season_tot_episodes, 
                                             self.episode_dict, self.series_runtime_data, 
                                             self.series_runtime_totals, self.season_info, 
                                             self.season_episodes]
        self.add_values(self.series_dict, self.series_imdb_id, addlist)

        # print(f"FINAL: SERIES_DICT: {self.series_dict}")
  
    def add_values(self, dic, key, list_of_values):
        if key not in dic:
            dic[key] = list()
        dic[key].extend(list_of_values)
        return dic
    
    def get__series_runtime_data(self):
        return self.series_runtime_data

    def get_episode_runtime(self, season_no, episode_no):
        return self.series_runtime_data[season_no][episode_no]

    def get_season_runtime(self, season_no):
        season_runtime = 0
        series_runtime_data = self.get__series_runtime_data()
        season = series_runtime_data[season_no]

        if season_no < len(season):
            for i in range(1, len(season)):
                if season[i] is not None:
                    season_runtime += int(season[i])

        return season_runtime


if __name__ == '__main__':
    si = SeriesInfo('tt8740790')
    # si = SeriesInfo('tt4574334')
    # print("test getting series runtime data")
    # print(si.get__series_runtime_data)
    # print("test getting episode data for season 1, episode 1")
    # print(si.get_episode_runtime(1, 1))
    # print("test getting runtime if no episode specified (=entire season?)")
    # print(si.get_season_runtime(1))


