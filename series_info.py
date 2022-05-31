from wiki import find_id, find_season_episodes
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
            for j in range(1, no_of_episodes + 1):
                episode_imdb_id = season_data['episodes'][j - 1]['id']
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

        if season_no < len(series_data):
            for i in range(1, len(season)):
                if season[i] is not None:
                    season_runtime += int(season[i])
                else:
                    pass
        return season_runtime

    def get_total_runtime(self):
        total_runtime = 0
        series_data = self.get__series_data()

        season_num = 1

        season = series_data[season_num]
        season_episode_list = self.__seasons_list

        if season_num <= len(season_episode_list):
            for i in range(0, len(season_episode_list)):
                for j in range(1, len(season)):
                    if season[j] is not None:
                        total_runtime += int(season[j])
                        if j >= (len(season) - 1):
                            season_num += 1
                            if season_num > len(season_episode_list):
                                break
                            else:
                                season = series_data[season_num]
                                j = 1
            return total_runtime, season_num


if __name__ == '__main__':
    # si = SeriesInfo('tt1865718')  # [Gravity Falls works/ Total also works]

    si = SeriesInfo('tt0944947') #[GoT works]
    # si = SeriesInfo('tt0303461') #[Firefly works]
    # si = SeriesInfo('tt0162065') #[Angel works/ Total also works]

    # si = SeriesInfo('tt8740790')
    print("_______________________________")
    print(len(si.get__series_data()) - 1)
    print(si.get_total_runtime())

    print("_______________________________")
    print(si.get__series_data())

    print("_______________________________")
    print(si.get_episode_runtime(1, 1))

    print("_______________testing 8 seasons________________")
    print(si.get_season_runtime(1))
    print(si.get_season_runtime(2))
    print(si.get_season_runtime(3))
    print(si.get_season_runtime(4))
    print(si.get_season_runtime(5))
    print(si.get_season_runtime(6))
    print(si.get_season_runtime(7))
    print(si.get_season_runtime(8))


