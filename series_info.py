from wiki import find_id, find_season_episodes
import isodate
import threading
import time


class SeriesInfo:
    def __init__(self, imdb_id):
        self.__series_imdb_id = imdb_id
        self.series_details = find_id(self.__series_imdb_id)
        self.series_title = self.series_details['title']
        self.__check_set_movie_series()
        self.__set_series_data()
        self.series_runtime_list = self.get_series_runtime_list()

    class MyThread(threading.Thread):
        def __init__(self, threadID, name, no_of_episodes, season_data, i, si):
            threading.Thread.__init__(self)
            self.threadID = threadID
            self.name = name
            self.no_of_episodes = no_of_episodes
            self.season_data = season_data
            self.i = i
            self.si = si

        def run(self):
            SeriesInfo.episode_date_loop(self.si, self.no_of_episodes, self.season_data, self.i)

    def __check_set_movie_series(self):

        if self.series_details['type'] == 'TVSeries':
            self.__seasons_list = self.series_details['tvSeriesInfo']['seasons']
            self.__series_data = ['0'] * (len(self.__seasons_list) + 1)
        elif self.series_details['type'] == 'Movie':
            self.__seasons_list = ['1']
            self.__series_data = ['0'] * (len(self.__seasons_list) + 1)
        else:
            self.__seasons_list = ['1']
            self.__series_data = ['0'] * (len(self.__seasons_list) + 1)

    def __set_series_data(self):
        run_time = 0
        if self.series_details['type'] == 'TVSeries':
            thread_list = []
            for i in self.__seasons_list:
                season_data = find_season_episodes(self.__series_imdb_id, i)
                if season_data["episodes"] is None:
                    break
                no_of_episodes = len(season_data["episodes"])
                self.__series_data[int(i)] = [None] * (no_of_episodes + 1)
                my_thread = self.MyThread(i, f"thread_{i}", no_of_episodes,season_data,i, self)
                thread_list.append(my_thread)
                # self.episode_date_loop(no_of_episodes, season_data, i)

            for thread in thread_list:
                thread.start()

            for thread in thread_list:
                thread.join()


        elif self.series_details['type'] == 'Movie':
            self.__series_data[[1][0]] = [0, int(self.series_details['runtimeMins'])]
        else:
            self.__series_data[[1][0]] = [0, 0]

    def episode_date_loop(self, no_of_episodes, season_data, i):
        for j in range(1, no_of_episodes + 1):
            episode_imdb_id = season_data['episodes'][j - 1]['id']
            try:
                run_time = find_id(episode_imdb_id)['runtimeMins']
            except Exception as e:
                print(Exception)
                break
            if run_time is not None:
                if run_time[0] == "P":
                    run_time = int(isodate.parse_duration(run_time).total_seconds() / 60)
                else:
                    run_time = int(run_time)
            else:
                try:
                    run_time = find_id(episode_imdb_id)['runtimeMins']
                except Exception as e:
                    print(Exception)
                    break
                if run_time is not None:
                    if run_time[0] == "P":
                        run_time = int(isodate.parse_duration(run_time).total_seconds() / 60)
                    else:
                        run_time = int(run_time)

            self.__series_data[int(i)][int(j)] = run_time

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

    def get_series_runtime_list(self):
        if self.series_details['type'] == 'TVSeries':
            series_data = self.get__series_data()
            series_runtime_list = [0] * len(series_data)
            for i in range(1, len(series_data)):
                series_runtime_list[i] = self.get_season_runtime(i)
            return series_runtime_list
        else:
            return self.__series_data[1]

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
            return total_runtime

    def get_season_list(self):
        return self.__seasons_list


if __name__ == '__main__':
    # si = SeriesInfo('tt1865718')  # [Gravity Falls works/ Total also works]
    startTime = time.time()
    si = SeriesInfo('tt0944947') #[GoT works]
    # si = SeriesInfo('tt0303461') #[Firefly works]
    # si = SeriesInfo('tt9612516') # Space Force
    # si = SeriesInfo('tt0110413')  # movie
    # si = SeriesInfo('tt0162065') #[Angel works/ Total also works]

    # si = SeriesInfo('tt8740790')
    print(si.series_title)
    print("_______________________________")
    print("No of seasons")
    print(len(si.get__series_data()) - 1)
    print("Total Series runtime")
    print(si.get_total_runtime())

    print("_______________________________")
    print("Series runtime details")
    print(si.get__series_data())

    print("_______________________________")
    print("season1, episode1 data")
    print(si.get_episode_runtime(1, 1))

    print("_______________testing 2 seasons________________")
    print(si.get_season_runtime(1))
    print(si.get_season_runtime(2))
    # print(si.get_season_runtime(3))
    # print(si.get_season_runtime(4))
    # print(si.get_season_runtime(5))
    # print(si.get_season_runtime(6))
    # print(si.get_season_runtime(7))
    # print(si.get_season_runtime(8))

    executionTime = (time.time() - startTime)
    print('Execution time in seconds: ' + str(executionTime))