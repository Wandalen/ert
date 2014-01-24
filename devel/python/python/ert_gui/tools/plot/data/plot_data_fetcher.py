from ert.enkf.plot import EnsembleDataFetcher, ObservationDataFetcher, RefcaseDataFetcher, BlockObservationDataFetcher
from ert.enkf.plot.ensemble_block_data_fetcher import EnsembleBlockDataFetcher
from ert_gui.tools.plot.data import PlotData, ObservationPlotData, EnsemblePlotData, RefcasePlotData
from ert_gui.models import ErtConnector
from ert_gui.models.mixins import ModelMixin


class PlotDataFetcher(ErtConnector, ModelMixin):

    def getPlotDataForKeyAndCases(self, key, cases):
        observation_data_fetcher = ObservationDataFetcher(self.ert())
        block_observation_data_fetcher = BlockObservationDataFetcher(self.ert())

        if self.isBlockObservationKey(key):
            return self.fetchBlockObservationData(block_observation_data_fetcher, key, cases)

        elif self.isSummaryKey(key):
            return self.fetchSummaryData(observation_data_fetcher, key, cases)

        else:
            raise NotImplementedError("Key %s not supported." % key)


    def isSummaryKey(self, key):
        ensemble_data_fetcher = EnsembleBlockDataFetcher(self.ert())
        return ensemble_data_fetcher.supportsKey(key)


    def isBlockObservationKey(self, key):
        block_observation_data_fetcher = BlockObservationDataFetcher(self.ert())
        return block_observation_data_fetcher.supportsKey(key)


    def fetchBlockObservationData(self, block_observation_data_fetcher, key, cases):
        plot_data = PlotData(key)

        data = block_observation_data_fetcher.fetchData(key)
        block_observation_plot_data = ObservationPlotData(key)
        selected_report_step_index = 0

        if len(data) > 0:
            data = data[selected_report_step_index]
            block_observation_plot_data.setObservationData(data["x"], data["y"], data["std"], False, histogram_support=False)
            block_observation_plot_data.updateBoundaries(data["min_x"], data["max_x"], data["min_y"], data["max_y"])

            plot_data.setObservationData(block_observation_plot_data)

            for case in cases:
                ensemble_data = EnsembleBlockDataFetcher(self.ert()).fetchData(key, case)

                if len(ensemble_data) > 0:
                    ensemble_data = ensemble_data[selected_report_step_index]
                    ensemble_plot_data = EnsemblePlotData(key, case)
                    ensemble_plot_data.setEnsembleData(ensemble_data["x"], ensemble_data["y"], ensemble_data["min_x_values"], ensemble_data["max_x_values"], histogram_support=False)
                    ensemble_plot_data.updateBoundaries(ensemble_data["min_x"], ensemble_data["max_x"], ensemble_data["min_y"], ensemble_data["max_y"])
                    plot_data.addEnsembleData(ensemble_plot_data)

        return plot_data

    def fetchSummaryData(self, observation_data_fetcher, key, cases):
        plot_data = PlotData(key)

        observation_data = observation_data_fetcher.fetchData(key)
        observation_plot_data = ObservationPlotData(key)
        observation_plot_data.setObservationData(observation_data["x"], observation_data["y"], observation_data["std"], observation_data["continuous"])
        observation_plot_data.updateBoundaries(observation_data["min_x"], observation_data["max_x"], observation_data["min_y"], observation_data["max_y"])
        plot_data.setObservationData(observation_plot_data)

        refcase_data = RefcaseDataFetcher(self.ert()).fetchData(key)
        refcase_plot_data = RefcasePlotData(key)
        refcase_plot_data.setRefcaseData(refcase_data["x"], refcase_data["y"])
        refcase_plot_data.updateBoundaries(refcase_data["min_x"], refcase_data["max_x"], refcase_data["min_y"], refcase_data["max_y"])

        plot_data.setRefcaseData(refcase_plot_data)

        for case in cases:
            ensemble_data = EnsembleDataFetcher(self.ert()).fetchData(key, case)

            ensemble_plot_data = EnsemblePlotData(key, case)
            ensemble_plot_data.setEnsembleData(ensemble_data["x"], ensemble_data["y"], ensemble_data["min_y_values"], ensemble_data["max_y_values"])
            ensemble_plot_data.updateBoundaries(ensemble_data["min_x"], ensemble_data["max_x"], ensemble_data["min_y"], ensemble_data["max_y"])
            plot_data.addEnsembleData(ensemble_plot_data)

        return plot_data