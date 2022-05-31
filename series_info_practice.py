from wiki2 import find_id, find_season_episodes
import isodate
from datetime import datetime, timedelta


class SeriesInfo:
    def __init__(self, imdb_id):
        self.__series_imdb_id = imdb_id
        self.__seasons_list = (find_id(self.__series_imdb_id))['tvSeriesInfo']['seasons']
        self.__series_data = ['0'] * (len(self.__seasons_list) + 1)
        self.__set_series_data()

    def __set_series_data(self):
        for i in self.__seasons_list:
            season_data = find_season_episodes(self.__series_imdb_id, i)
            if season_data["episodes"] is None:
                break
            no_of_episodes = len(season_data["episodes"])
            self.__series_data[int(i)] = [None] * (no_of_episodes + 1)
            for j in range(1, no_of_episodes+1):
                episode_imdb_id = season_data['episodes'][j-1]['id']
                try:
                    run_time = find_id(episode_imdb_id)['runtimeMins']
                    if run_time is None:
                        break
                except Exception as e:
                    print(Exception)
                    break
                if run_time[0] == "P":
                    run_time = int(isodate.parse_duration(run_time).total_seconds() / 60)
                else:
                    run_time = int(run_time)
                self.__series_data[int(i)][int(j)] = run_time

        print(self.__series_data)

    def get__series_data(self):
        return self.__series_data

    def get_episode_runtime(self, season_no, episode_no):
        return self.__series_data[season_no][episode_no]

    def get_season_runtime(self, season_no):
        season_runtime = 0
        series_data = self.get__series_data()
        season = series_data[season_no]

        if season_no < len(season):
            for i in range(1, len(season)):
                if season[i] is not None:
                    season_runtime += int(season[i])
        return season_runtime


if __name__ == '__main__':
    si = SeriesInfo('tt8740790')
    print(si.get__series_data())
    print(si.get_episode_runtime(1, 1))
    print(si.get_season_runtime(2))
